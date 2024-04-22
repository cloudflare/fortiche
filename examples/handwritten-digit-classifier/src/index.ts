import {load} from '../output/index.mjs'
import weights from '../mnist.bin'

import indexHtml from './www/index.html'
import indexJs from './www/index.js.txt'
import styleCss from './www/style.css'

let weights_ptr = null;
let program = null;

export default {
    async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
        const {pathname} = new URL(request.url);

        if (pathname === "/") {
            const headers = {
                "content-type": "text/html",
            };
            return new Response(indexHtml, { headers });
        }
        if (pathname === "/index.js") {
            const headers = {
                "content-type": "text/javascript",
            };
            return new Response(indexJs, { headers });
        }
        if (pathname === "/style.css") {
            const headers = {
                "content-type": "text/css",
            };
            return new Response(styleCss, { headers });
        }

        try {
            if (program === null) {
                program = await load();

                const floats = new Float64Array(weights);

                weights_ptr = program.malloc(floats.byteLength);
                program.HEAPF64.set(floats, weights_ptr / 8);
            }

            const image = new Float64Array(await request.arrayBuffer());

            const image_ptr = program.malloc(28 * 28 * 8);
            program.HEAPF64.set(image, image_ptr / 8);

            const out_ptr = program.malloc(10 * 8);

            program.classifier(weights_ptr, image_ptr, out_ptr);

            const out_bytes = program.HEAPF64.subarray(out_ptr / 8, out_ptr / 8 + 10);
            const out = [...out_bytes];

            // Wasm memory cleanup
            program.free(image_ptr);
            program.free(out_ptr);

            return new Response(JSON.stringify(out) || "", {
                status: 200,
                headers: {
                    "content-type": "application/json",
                }
            })
        } catch (err) {
            console.log(err.stack);
            return new Response("an error occurred")
        }
    },
};

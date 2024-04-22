// Import what Fortiche generated
import {load} from "../output/index.mjs"

export default {
    async fetch(request: Request): Promise<Response> {
        // Load the Fortran program
        const program = await load();

        // Allocate space in memory for the arguments and result
        const aPtr = program.malloc(4);
        const bPtr = program.malloc(4);
        const outPtr = program.malloc(4);

        // Set argument values
        program.HEAP32[aPtr / 4] = 123;
        program.HEAP32[bPtr / 4] = 321;

        // Run the Fortran add subroutine
        program.add(aPtr, bPtr, outPtr);

        // Read the result
        const res = program.HEAP32[outPtr / 4];

        // Free everything
        program.free(aPtr);
        program.free(bPtr);
        program.free(outPtr);

        return Response.json({ res });
    },
};

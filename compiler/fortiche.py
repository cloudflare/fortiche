import argparse
import json
import subprocess

parser = argparse.ArgumentParser(
        prog='fortiche', description='Fortran compiler for Cloudflare Workers')
parser.add_argument('files', type=str, nargs='+', help='Fortan source files')
parser.add_argument('--export-func', type=str, action='append',
                    help='Fortran subroutine(s) to be exported to JavaScript')
parser.add_argument("--with-BLAS-3-12-0", action="store_true",
                    help="Compile with BLAS 3.12.0")
parser.add_argument("--with-LAPACK-3-12-0", action="store_true",
                    help="Compile with LAPACK 3.12.0")
parser.add_argument("--stack-size", default="4Mb",
                    help="Stack size (default: 4Mb)")
parser.add_argument("--verbose", action="store_true",
                    help="Enable verbose mode")


args = parser.parse_args()

if args.verbose:
    print(args)


def compile_flang(args):
    command = [
        "/llvm/build/bin/flang-new",
        "-g", "-O2",
        "-o", "/tmp/out.o",
        "-c",
        *args.files,
    ]

    if args.verbose:
        print(command)

    subprocess.run(command, cwd="/input")


def generate_post_js(args):
    buffer = ""

    buffer += "Module['malloc'] = Module['_malloc'];"
    buffer += "Module['free'] = Module['_free'];"

    if args.export_func:
        for export_func in args.export_func:
            buffer += f"Module['{export_func}'] = Module['_{export_func}_'];"

    if args.verbose:
        print("========== post-js ==========")
        print(buffer)
        print("========== post-js ==========")

    f = open("/tmp/post-js.js", "w+")
    f.write(buffer)
    f.close()


def generate_index_js(args):
    f = open("/output/index.mjs", "w+")

    f.write("""
import loadEmscripten from './out.mjs'
import wasm from './out.wasm'

export async function load() {
    return loadEmscripten({
        locateFile(what) {
            return null;
        },

        instantiateWasm(info, receive) {
            const instance = new WebAssembly.Instance(wasm, info)
            receive(instance)
            return instance.exports
        },
    });
}
    """)

    f.close()


def compile_emcc(args):
    exported_functions = ['_malloc', '_free']

    if args.export_func:
        export_func = map(lambda name: f"_{name}_", args.export_func)
        exported_functions.extend(export_func)

    exported_functions = json.dumps(exported_functions)

    command = [
        "emcc",
        "/llvm/build/flang/runtime/libFortranRuntime.a"
    ]

    if args.with_BLAS_3_12_0:
        command.extend([
            "/BLAS/blas_LINUX.a",
        ])

    if args.with_LAPACK_3_12_0:
        command.extend([
            "/lapack/liblapack.a",
        ])

    command.extend([
        "/tmp/out.o",
        "--pre-js", "/compiler/pre-em.js",
        "--post-js", "/tmp/post-js.js",
        "-o", "/output/out.mjs",
        "-sENVIRONMENT=web", "-sMODULARIZE=1",
        f"-sSTACK_SIZE={args.stack_size}",
        "-sNO_FILESYSTEM", "-sALLOW_MEMORY_GROWTH=1",
        f"-sEXPORTED_FUNCTIONS={exported_functions}",
        "-Oz", "-g"
    ])

    if args.verbose:
        print(command)

    subprocess.run(command)


compile_flang(args)
generate_post_js(args)
compile_emcc(args)
generate_index_js(args)

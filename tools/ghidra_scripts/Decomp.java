// Decompile functions containing the given addresses (or named functions) into a text file.
// args: <outfile> <addr|name> [<addr|name> ...]
import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.*;
import ghidra.program.model.address.*;
import ghidra.program.model.listing.*;
import ghidra.program.model.symbol.*;
import java.io.*;

public class Decomp extends GhidraScript {
    @Override
    public void run() throws Exception {
        String[] a = getScriptArgs();
        PrintWriter out = new PrintWriter(new FileWriter(a[0], true));
        DecompInterface d = new DecompInterface();
        d.openProgram(currentProgram);
        FunctionManager fm = currentProgram.getFunctionManager();
        for (int i = 1; i < a.length; i++) {
            Function f = null;
            try {
                Address ad = currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(a[i]);
                f = fm.getFunctionContaining(ad);
                if (f == null) {
                    disassemble(ad);
                    createFunction(ad, null);
                    f = fm.getFunctionContaining(ad);
                }
            } catch (Exception e) {
                for (Symbol s : currentProgram.getSymbolTable().getSymbols(a[i])) {
                    f = fm.getFunctionAt(s.getAddress());
                    if (f != null) break;
                }
            }
            if (f == null) { out.println("// no function for " + a[i]); continue; }
            DecompileResults r = d.decompileFunction(f, 120, monitor);
            out.println("// ===== " + a[i] + " -> " + f.getName() + " @ " + f.getEntryPoint());
            out.println(r.decompileCompleted() ? r.getDecompiledFunction().getC() : "// FAILED " + r.getErrorMessage());
        }
        out.close();
    }
}

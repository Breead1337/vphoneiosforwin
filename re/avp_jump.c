// ===== 0x00105374 -> FUN_00105374 @ 00105374

void FUN_00105374(ulong param_1,undefined8 param_2,undefined8 param_3)

{
  CallSupervisor(6);
  FUN_00104728(param_1 & 0xffffffff);
  FUN_0012785c(s_boot_breadcrumbs_0014674d,s_boot_breadcrumbs_0014674d,s__llx__d_0014675e,
               &PTR_LOOP_0013ce88);
  FUN_00104438(param_1);
  FUN_00104150(1,0);
  FUN_00104404(param_1);
  FUN_001185a8();
  FUN_00111774();
  FUN_001053f4(param_2,param_3,param_1 & 0xffffffff);
  CallSupervisor(7);
                    /* WARNING: Subroutine does not return */
  FUN_0010550c();
}



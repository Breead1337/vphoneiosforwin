// ===== 0x00124a94 -> FUN_00124a94 @ 00124a94

void FUN_00124a94(undefined8 param_1,undefined8 param_2,ulong param_3)

{
  code *pcVar1;
  undefined1 in_CY;
  ulong uVar2;
  undefined8 extraout_x8;
  code *UNRECOVERED_JUMPTABLE;
  ulong unaff_x30;
  
  FUN_0012605c();
  uVar2 = FUN_001261f8();
  if (!(bool)in_CY || param_3 <= uVar2) {
                    /* WARNING: Subroutine does not return */
    FUN_0012ea7c();
  }
  if (*(long *)(uVar2 + 0x60) != 0) {
    FUN_001261c0();
    FUN_00126038(extraout_x8);
    if (((unaff_x30 ^ unaff_x30 << 1) >> 0x3e & 1) != 0) {
                    /* WARNING: Does not return */
      pcVar1 = (code *)SoftwareBreakpoint(0xc471,0x124af8);
      (*pcVar1)();
    }
                    /* WARNING: Could not recover jumptable at 0x00124af8. Too many branches */
                    /* WARNING: Treating indirect jump as call */
    (*UNRECOVERED_JUMPTABLE)();
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_0012e944();
}



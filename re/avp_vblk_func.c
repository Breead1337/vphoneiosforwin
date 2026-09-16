// ===== 0x00107b80 -> FUN_00107b80 @ 00107b80

void FUN_00107b80(undefined8 param_1,undefined8 param_2,ulong param_3)

{
  undefined8 unaff_x19;
  undefined4 *unaff_x20;
  undefined8 unaff_x30;
  undefined1 auVar1 [16];
  undefined1 uStack000000000000000c;
  
  auVar1 = FUN_00107e08();
  *unaff_x20 = 0;
  if (auVar1._8_8_ <= auVar1._0_8_ && auVar1._0_8_ < param_3) {
    FUN_00107db0();
    uStack000000000000000c = 1;
    FUN_00107d80();
    FUN_0010dca4();
    uStack000000000000000c = 1;
    FUN_00107d80();
    FUN_0010dca4();
    uStack000000000000000c = 0;
    FUN_00107d80();
    FUN_0010dca4();
    FUN_00107d80();
    FUN_0010dd5c();
    if (*(char *)(unaff_x20 + 4) != '\0') {
      FUN_00127704(0x40200103);
      unaff_x19 = 0xffffffff;
    }
    FUN_00107dd0(unaff_x19,unaff_x30);
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_0012ea7c();
}



// ===== 0x106674 -> FUN_00106674 @ 00106674

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_00106674(undefined8 param_1,undefined8 param_2,ulong param_3)

{
  undefined8 uVar1;
  undefined1 uVar2;
  bool bVar3;
  ulong uVar4;
  undefined1 auVar5 [16];
  
  FUN_00106af0();
  uVar1 = _DAT_7002add8;
  auVar5 = FUN_00106bc4();
  uVar4 = auVar5._0_8_;
  bVar3 = auVar5._8_8_ <= uVar4;
  uVar2 = bVar3 && uVar4 == param_3;
  if (!bVar3 || param_3 <= uVar4) {
                    /* WARNING: Subroutine does not return */
    FUN_0012ea7c();
  }
  FUN_0010d450();
  FUN_00106b20(uVar1);
  if ((bool)uVar2) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00123c18();
}


// ===== 0x106748 -> FUN_00106748 @ 00106748

long FUN_00106748(undefined2 param_1,long param_2,long *param_3)

{
  long *plVar1;
  undefined1 auVar2 [16];
  
  auVar2 = FUN_00106bc4(param_1);
  plVar1 = auVar2._0_8_;
  if (auVar2._8_8_ <= plVar1 && plVar1 < param_3) {
    return *plVar1 + param_2;
  }
                    /* WARNING: Subroutine does not return */
  FUN_0012ea7c();
}


// ===== 0x106788 -> FUN_00106788 @ 00106788

long FUN_00106788(undefined2 param_1,long param_2,ulong param_3)

{
  ulong uVar1;
  undefined1 auVar2 [16];
  
  auVar2 = FUN_00106bc4(param_1);
  uVar1 = auVar2._0_8_;
  if (auVar2._8_8_ <= uVar1 && uVar1 < param_3) {
    return *(long *)(uVar1 + 0x10) + param_2;
  }
                    /* WARNING: Subroutine does not return */
  FUN_0012ea7c();
}


// ===== 0x1061e4 -> FUN_001061e4 @ 001061e4

void FUN_001061e4(undefined8 param_1)

{
  FUN_00106b0c(param_1,&LAB_00106398,0,0,0,0);
  return;
}



// ===== 0x00118390 -> FUN_00118390 @ 00118390

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined8 FUN_00118390(void)

{
  int iVar1;
  undefined8 uVar2;
  undefined1 auVar3 [16];
  ulong local_30 [4];
  
  local_30[2] = 0;
  local_30[3] = 0;
  local_30[0] = 0;
  local_30[1] = 0;
  FUN_0011f80c(local_30);
  if (local_30[2] <= local_30[0]) {
                    /* WARNING: Subroutine does not return */
    FUN_0012ea7c();
  }
  local_30[0] = *(ulong *)(local_30[0] + 0x18);
  auVar3 = thunk_FUN_0011857c();
  if (auVar3._0_8_ == 0) {
    iVar1 = FUN_00118344();
    auVar3._8_8_ = _DAT_700301c8;
    auVar3._0_8_ = _DAT_700301c0;
    if ((iVar1 == 0) || (_DAT_700301c0 == 0)) {
      return 0;
    }
  }
  uVar2 = thunk_FUN_0011857c(auVar3._0_8_,auVar3._8_8_);
  return uVar2;
}



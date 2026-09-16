// ===== 0x00107e34 -> FUN_00107e34 @ 00107e34

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_00107e34(long param_1)

{
  undefined8 uVar1;
  char *local_68;
  undefined8 uStack_60;
  char *local_58;
  undefined8 uStack_50;
  long local_48;
  
  local_48 = _DAT_7002add8;
  if (param_1 == 0) {
    uVar1 = 0x16;
  }
  else {
    local_58 = (char *)0x0;
    uStack_50 = 0;
    local_68 = (char *)0x0;
    uStack_60 = 0;
    FUN_00105288(&local_68);
    if (local_58 <= local_68) {
                    /* WARNING: Subroutine does not return */
      FUN_0012ea7c();
    }
    CallSupervisor(0xc5);
    if (*local_68 == '\0') {
      FUN_00107ef8();
      uVar1 = FUN_0010d278();
    }
    else {
      FUN_00107ef8();
      uVar1 = FUN_001079a4();
    }
  }
  if (_DAT_7002add8 == local_48) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00123c18(uVar1);
}



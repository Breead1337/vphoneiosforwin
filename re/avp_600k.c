// ===== 0x104868 -> FUN_00104868 @ 00104868

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined8
FUN_00104868(undefined4 *param_1,undefined4 *param_2,undefined4 *param_3,undefined8 param_4,
            ulong param_5)

{
  undefined8 uVar1;
  undefined4 *puVar2;
  undefined4 *puVar3;
  undefined4 *puVar4;
  undefined4 *puVar5;
  undefined4 uVar6;
  
  if ((param_1 == (undefined4 *)0x0) || ((param_5 & 3) != 0)) {
                    /* WARNING: Subroutine does not return */
    FUN_0010550c();
  }
  if ((_DAT_006000d4 & 1) == 0) {
    uVar1 = 0xffffffff;
  }
  else {
    puVar2 = param_1;
    puVar4 = (undefined4 *)&DAT_00600090;
    do {
      if (puVar4 < (undefined4 *)0x6000d1) {
        if (puVar4 < &DAT_00600090) {
LAB_001048f8:
                    /* WARNING: Subroutine does not return */
          FUN_0012ea7c();
        }
        puVar5 = puVar4 + 1;
        uVar6 = *puVar4;
        if (puVar2 < param_2 || param_3 <= puVar2) goto LAB_001048f8;
      }
      else {
        if (puVar2 < param_2 || param_3 <= puVar2) goto LAB_001048f8;
        uVar6 = 0;
        puVar5 = puVar4;
      }
      puVar3 = puVar2 + 1;
      *puVar2 = uVar6;
      puVar2 = puVar3;
      puVar4 = puVar5;
    } while (puVar3 < (undefined4 *)((long)param_1 + param_5));
    uVar1 = 0;
  }
  return uVar1;
}


// ===== 0x1048fc -> FUN_001048fc @ 001048fc

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_001048fc(void)

{
  if ((_DAT_006000d4 >> 0x10 & 1) == 0) {
    _DAT_006000d4 = _DAT_006000d4 | 0x10000;
    thunk_FUN_001003f0();
    if ((_DAT_006000d4 >> 0x10 & 1) != 0) {
      return;
    }
  }
                    /* WARNING: Subroutine does not return */
  FUN_0010550c();
}


// ===== 0x104944 -> FUN_00104944 @ 00104944

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_00104944(undefined4 *param_1,undefined4 *param_2,undefined4 *param_3,undefined8 param_4,
                 ulong param_5,undefined4 param_6)

{
  undefined4 uVar1;
  bool bVar2;
  undefined4 *puVar3;
  undefined4 *puVar4;
  undefined4 *puVar5;
  
  if ((_DAT_006000d4 >> 0x10 & 1) != 0) {
LAB_001049d0:
                    /* WARNING: Subroutine does not return */
    FUN_0010550c();
  }
  if (param_1 == (undefined4 *)0x0) {
    for (puVar3 = (undefined4 *)&DAT_00600090; puVar3 < (undefined4 *)0x6000d1; puVar3 = puVar3 + 1)
    {
      *puVar3 = 0;
    }
    _DAT_006000d4 = _DAT_006000d4 & 0xfffffffe;
  }
  else {
    bVar2 = false;
    puVar3 = param_1;
    puVar4 = (undefined4 *)&DAT_00600090;
    do {
      while (puVar3 < (undefined4 *)((long)param_1 + (param_5 & 0xfffffffffffffffc))) {
        if (puVar3 < param_2 || param_3 <= puVar3) {
                    /* WARNING: Subroutine does not return */
          FUN_0012ea7c();
        }
        puVar5 = puVar4 + 1;
        *puVar4 = *puVar3;
        puVar3 = puVar3 + 1;
        puVar4 = puVar5;
        if ((undefined4 *)0x6000d0 < puVar5) {
          if (!bVar2) goto LAB_001049d0;
          goto LAB_001049bc;
        }
      }
      uVar1 = 0;
      if (!bVar2) {
        uVar1 = param_6;
      }
      puVar5 = puVar4 + 1;
      *puVar4 = uVar1;
      bVar2 = true;
      puVar4 = puVar5;
    } while (puVar5 < (undefined4 *)0x6000d1);
LAB_001049bc:
    _DAT_006000d4 = _DAT_006000d4 | 1;
  }
  return;
}


// ===== 0x104a90 -> FUN_00104a90 @ 00104a90

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_00104a90(void)

{
  _DAT_00600400 = _DAT_00600400 | 1;
  FUN_00104cf0(0x18);
  return;
}


// ===== 0x104aac -> FUN_00104aac @ 00104aac

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_00104aac(void)

{
  _DAT_00600400 = _DAT_00600400 | 2;
  FUN_00104cf0(0x16);
  return;
}


// ===== 0x104cf0 -> FUN_00104cf0 @ 00104cf0

void FUN_00104cf0(uint param_1)

{
  FUN_0010420c(param_1 & 0xffff | 0xa0000);
  return;
}


// ===== 0x1043ac -> FUN_001043ac @ 001043ac

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_001043ac(void)

{
  int iVar1;
  
  _DAT_00400304 = 0;
  _DAT_00400308 = 0;
  _DAT_0040030c = 0;
  _DAT_00400300 = 0;
  iVar1 = thunk_FUN_00105244();
  _DAT_00400300 = _DAT_00400300 | iVar1 << 0x18;
  return;
}


// ===== 0x104438 -> FUN_00104438 @ 00104438

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_00104438(int param_1)

{
  int iVar1;
  ulong uVar2;
  
  if ((param_1 == 3) && ((char)DAT_7002af9c < '\0')) {
    DAT_7002af9c = DAT_7002af9c & 0x7f;
                    /* WARNING: Subroutine does not return */
    FUN_0010550c();
  }
  if (param_1 == 0) {
    FUN_00123dc8();
  }
  else {
    if (param_1 != 2) goto LAB_001044d4;
    FUN_001123cc(0x3c505144,0);
    FUN_00123dc8();
    FUN_001123cc(0x3e505144,0);
  }
  FUN_00105cdc(0x40000);
  uVar2 = FUN_00105cdc(0x80000);
  if ((uVar2 & 1) == 0) {
    _DAT_00400328 = 0;
    _DAT_0040032c = 0;
  }
  iVar1 = FUN_00106d50();
  if (iVar1 == 0) {
    return;
  }
LAB_001044d4:
                    /* WARNING: Subroutine does not return */
  FUN_0010550c();
}


// ===== 0x1044d8 -> FUN_001044d8 @ 001044d8

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_001044d8(int param_1,uint param_2)

{
  if ((param_2 != 0 || param_1 != 0) && ((param_2 & 1) != 0)) {
    _DAT_00400328 = 0;
    _DAT_0040032c = 0;
  }
  return;
}


// ===== 0x1047c8 -> FUN_001047c8 @ 001047c8

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined8 FUN_001047c8(long param_1,undefined8 param_2,undefined4 *param_3)

{
  undefined4 *puVar1;
  undefined4 *puVar2;
  undefined1 auVar3 [16];
  
  if (param_1 == 0) {
    for (puVar1 = (undefined4 *)&DAT_00400330; puVar1 < (undefined4 *)0x40035d; puVar1 = puVar1 + 1)
    {
      *puVar1 = 0;
    }
    _DAT_00400300 = _DAT_00400300 & 0xffffffef;
  }
  else {
    auVar3 = thunk_FUN_00104d10();
    puVar2 = auVar3._0_8_;
    for (puVar1 = (undefined4 *)&DAT_00400330; puVar1 < (undefined4 *)0x40035d; puVar1 = puVar1 + 1)
    {
      if (auVar3._0_8_ < auVar3._8_8_ || param_3 <= puVar2) {
                    /* WARNING: Subroutine does not return */
        FUN_0012ea7c();
      }
      *puVar1 = *puVar2;
      puVar2 = puVar2 + 1;
    }
    _DAT_00400300 = _DAT_00400300 | 0x10;
  }
  return 0;
}


// ===== 0x104a04 -> FUN_00104a04 @ 00104a04

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

uint FUN_00104a04(void)

{
  return _DAT_00400300 >> 3 & 1;
}


// ===== 0x104a18 -> FUN_00104a18 @ 00104a18

void FUN_00104a18(void)

{
  FUN_00104d08();
  return;
}


// ===== 0x104d4c -> FUN_00104d4c @ 00104d4c

void FUN_00104d4c(void)

{
  return;
}


// ===== 0x104340 -> FUN_00104340 @ 00104340

void FUN_00104340(void)

{
  FUN_00104d08();
  return;
}


// ===== 0x1045d0 -> FUN_001045d0 @ 001045d0

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

bool FUN_001045d0(int param_1,undefined4 *param_2,undefined4 *param_3,undefined4 *param_4,
                 undefined8 param_5,undefined4 *param_6,undefined4 *param_7,undefined4 *param_8,
                 undefined8 param_9,undefined4 *param_10,undefined4 *param_11,undefined4 *param_12)

{
  uint uVar1;
  
  uVar1 = (_DAT_00400300 >> 8 & 0xff) - 1;
  if (uVar1 < 2) {
    if (((param_2 < param_3 || param_4 <= param_2) ||
        (*param_2 = 0xe, param_6 < param_7 || param_8 <= param_6)) ||
       (*param_6 = 0, param_10 < param_11 || param_12 <= param_10)) {
                    /* WARNING: Subroutine does not return */
      FUN_0012ea7c();
    }
    *param_10 = 0;
    if (param_1 != 0) {
      *param_2 = 6;
      *param_10 = 0;
    }
    FUN_00104214(0x20004,*param_2,*param_6,0);
  }
  return uVar1 < 2;
}



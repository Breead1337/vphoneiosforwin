// ===== 0x001045d0 -> FUN_001045d0 @ 001045d0

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


// ===== 0x00104678 -> FUN_00104678 @ 00104678

void FUN_00104678(undefined8 param_1,undefined8 param_2,undefined8 param_3)

{
  code *pcVar1;
  ulong unaff_x30;
  
  FUN_00104214(0x20005,param_2,param_1,param_3);
  if (((unaff_x30 ^ unaff_x30 << 1) >> 0x3e & 1) != 0) {
                    /* WARNING: Does not return */
    pcVar1 = (code *)SoftwareBreakpoint(0xc471,0x1046c0);
    (*pcVar1)();
  }
  FUN_0010420c(0x20006);
  return;
}


// ===== 0x00126fa8 -> FUN_00126fa8 @ 00126fa8

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined4
FUN_00126fa8(undefined8 param_1,undefined8 param_2,undefined8 param_3,undefined8 param_4,
            undefined4 param_5)

{
  int iVar1;
  
  _DAT_70030af0 = FUN_00127548();
  _DAT_70030ae0 = param_5;
  _DAT_70030b00 = param_3;
  _DAT_70030b08 = param_4;
  iVar1 = thunk_FUN_0010c530();
  if (iVar1 == 0) {
    FUN_0010420c(0x20020);
    while ((DAT_70030ad2 & 1) == 0) {
      FUN_00123b00(_DAT_70030ad4);
    }
  }
  FUN_0010c420();
  return _DAT_70030adc;
}


// ===== 0x00124804 -> FUN_00124804 @ 00124804

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_00124804(undefined8 param_1,undefined8 param_2,ulong param_3)

{
  long lVar1;
  undefined1 in_CY;
  long lVar2;
  ulong uVar3;
  
  lVar1 = _DAT_7002add8;
  lVar2 = FUN_001248a0();
  if (lVar2 == 0) {
    FUN_00126104();
  }
  else {
    uVar3 = FUN_00126160();
    if (!(bool)in_CY || param_3 <= uVar3) {
                    /* WARNING: Subroutine does not return */
      FUN_0012ea7c();
    }
    FUN_001261b4();
  }
  if (_DAT_7002add8 == lVar1) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00123c18();
}


// ===== 0x00126a58 -> FUN_00126a58 @ 00126a58

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_00126a58(void)

{
  long lVar1;
  
  lVar1 = _DAT_7002add8;
  FUN_00126494();
  if (_DAT_7002add8 == lVar1) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00123c18();
}



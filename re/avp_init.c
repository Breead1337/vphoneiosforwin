// ===== 0x001042bc -> FUN_001042bc @ 001042bc

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined8 FUN_001042bc(void)

{
  _DAT_10000000 = 3;
  if ((_DAT_10010014 >> 2 & 1) != 0) {
    _DAT_10010014 = _DAT_10010014 & 0xfffffff9;
  }
  _DAT_10020080 = 0xf7ffffff;
  _DAT_10020100 = 0x8000000;
  CallSupervisor(0xa1);
  FUN_00118654();
  FUN_00104140();
  FUN_00104d1c(&DAT_0014673b);
  FUN_00107e34();
  FUN_00104bbc(1);
  return 0;
}


// ===== 0x00104580 -> FUN_00104580 @ 00104580

undefined8 FUN_00104580(void)

{
  FUN_00105280();
  FUN_0010414c();
  FUN_00104d1c(&DAT_00146748);
  FUN_00107e34();
  FUN_00104bbc(0);
  return 0;
}



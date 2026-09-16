// ===== 0x001262f8 -> FUN_001262f8 @ 001262f8

void FUN_001262f8(void)

{
  code *pcVar1;
  ulong unaff_x30;
  
  FUN_001269b4();
  FUN_00124760();
  FUN_001269a0();
  if (((unaff_x30 ^ unaff_x30 << 1) >> 0x3e & 1) != 0) {
                    /* WARNING: Does not return */
    pcVar1 = (code *)SoftwareBreakpoint(0xc471,0x126334);
    (*pcVar1)();
  }
  FUN_00124a94();
  return;
}


// ===== 0x00100e04 -> FUN_00100e04 @ 00100e04

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_00100e04(void)

{
  ulong *puVar1;
  undefined1 uVar2;
  int iVar3;
  long lVar4;
  undefined8 uVar5;
  ulong uVar6;
  ulong uVar7;
  ulong *puVar8;
  ulong *puVar9;
  ulong in_x4;
  undefined8 extraout_x8;
  undefined8 extraout_x8_00;
  ulong *puVar10;
  ulong unaff_x19;
  ulong unaff_x20;
  ulong unaff_x21;
  undefined1 auVar11 [16];
  undefined4 uStack0000000000000034;
  undefined4 uStack0000000000000044;
  undefined4 uStack000000000000007c;
  ulong in_stack_000000f0;
  ulong in_stack_000000f8;
  undefined4 in_stack_00000100;
  
  FUN_00102c3c();
  lVar4 = FUN_00102b58();
  uStack0000000000000034 = in_stack_00000100;
  FUN_00102af4();
  uVar5 = FUN_0012c8c0(0);
  puVar9 = (ulong *)0x1e;
  thunk_FUN_0012c6a8(uVar5,1);
  thunk_FUN_00102b40();
  uStack0000000000000044 = 0;
  uStack000000000000007c = 0;
  FUN_00102b04();
  uVar6 = FUN_00126910();
  uVar2 = in_stack_000000f8 == uVar6;
  if (in_stack_000000f8 < uVar6) {
    FUN_00102b04();
    uVar6 = in_stack_000000f0;
    uVar7 = FUN_00126910();
    uVar2 = uVar7 - in_stack_000000f8 == 0x1e;
    if ((long)(uVar7 - in_stack_000000f8) < 0x1e) goto LAB_00101098;
    if (lVar4 == 0) {
      FUN_00102b04();
      uVar6 = in_stack_000000f0;
      iVar3 = FUN_001262f8();
      uVar2 = iVar3 == 0x1e;
      if (!(bool)uVar2) goto LAB_00101098;
    }
    else {
      uVar2 = in_x4 == 0x1d;
      if (in_x4 < 0x1e) goto LAB_001010c4;
      FUN_00102bc0();
      FUN_00111154();
    }
    FUN_00102bc0();
    iVar3 = FUN_00100984();
    if ((iVar3 == 0) &&
       (uVar2 = uVar7 == in_stack_000000f8, uVar7 != in_stack_000000f8 || (bool)uVar2)) {
      uVar5 = FUN_0012c8c0(0);
      thunk_FUN_0012c768(uVar5,0x700283f0);
      auVar11 = FUN_00102ab4();
      puVar8 = auVar11._0_8_;
      if (auVar11._8_8_ <= puVar8 && puVar8 < puVar9) {
        puVar10 = puVar8 + 8;
        *puVar10 = unaff_x21;
        puVar8[9] = unaff_x20;
        puVar8[10] = unaff_x19;
        puVar8[0xb] = in_stack_000000f0;
        puVar8[0xc] = in_stack_000000f8;
        *(undefined4 *)(puVar8 + 0xd) = 0;
        *(undefined4 *)((long)puVar8 + 0x6c) = uStack000000000000007c;
        *(undefined4 *)(puVar8 + 0xe) = 0x696d6734;
        *(undefined4 *)((long)puVar8 + 0x74) = uStack0000000000000034;
        *(undefined1 (*) [16])(puVar8 + 0xf) = auVar11;
        puVar8[0x11] = (ulong)puVar9;
        puVar8[0x12] = uVar6;
        uVar6 = _DAT_700284a8;
        puVar1 = _DAT_70028498;
        puVar9 = _DAT_70028490;
        if ((_DAT_700284b0 == (undefined8 *)0x0) || (_DAT_70028490 == (ulong *)0x0)) {
LAB_001010c4:
                    /* WARNING: Subroutine does not return */
          FUN_0010550c();
        }
        if (_DAT_700284b8 <= _DAT_700284b0 && _DAT_700284b0 < _DAT_700284c0) {
          if ((undefined1 *)*_DAT_700284b0 != &DAT_70028490) goto LAB_001010c4;
          if (_DAT_70028498 <= _DAT_70028490 && _DAT_70028490 < _DAT_700284a0) {
            if ((undefined1 *)_DAT_70028490[4] != &DAT_70028490) goto LAB_001010c4;
            puVar8[2] = (ulong)_DAT_700284a0;
            puVar8[3] = uVar6;
            *puVar8 = (ulong)puVar9;
            puVar8[1] = (ulong)puVar1;
            puVar8[4] = (ulong)&DAT_70028490;
            puVar8[5] = (ulong)&DAT_70028490;
            puVar8[6] = 0x700284d0;
            puVar8[7] = (ulong)&PTR_LOOP_0013cf08;
            uVar2 = _DAT_70028498 <= _DAT_70028490 && _DAT_70028490 == _DAT_700284a0;
            if (_DAT_70028498 <= _DAT_70028490 && _DAT_70028490 < _DAT_700284a0) {
              _DAT_70028490[4] = (ulong)puVar8;
              _DAT_70028490[5] = (ulong)puVar8;
              _DAT_70028490[6] = (ulong)puVar10;
              _DAT_70028490[7] = 0x70028418;
              uStack0000000000000044 = 1;
              _DAT_700284a8 = 0x70028418;
              _DAT_70028490 = puVar8;
              _DAT_70028498 = puVar8;
              _DAT_700284a0 = puVar10;
              goto LAB_00101098;
            }
          }
        }
      }
                    /* WARNING: Subroutine does not return */
      FUN_0012ea7c();
    }
  }
LAB_00101098:
  FUN_00102bc0();
  FUN_001184fc();
  FUN_00102ad0(extraout_x8_00);
  if (!(bool)uVar2) {
                    /* WARNING: Subroutine does not return */
    FUN_00123c18();
  }
  FUN_00102c20(uStack0000000000000044,extraout_x8);
  return;
}


// ===== 0x00126214 -> FUN_00126214 @ 00126214

undefined8 FUN_00126214(undefined8 param_1,undefined8 param_2,ulong param_3)

{
  ulong uVar1;
  undefined8 uVar2;
  undefined1 auVar3 [16];
  
  auVar3 = FUN_001247ac();
  uVar1 = auVar3._0_8_;
  if (uVar1 == 0) {
    uVar2 = 0xffffffff;
  }
  else {
    if (uVar1 < auVar3._8_8_ || param_3 <= uVar1) {
                    /* WARNING: Subroutine does not return */
      FUN_0012ea7c();
    }
    uVar2 = 0;
    *(undefined1 *)(uVar1 + 0x98) = 1;
  }
  return uVar2;
}



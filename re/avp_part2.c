// ===== 0x00110cf0 -> FUN_00110cf0 @ 00110cf0

void FUN_00110cf0(undefined8 *param_1,undefined8 *param_2,ulong param_3)

{
  undefined8 uVar1;
  undefined8 uVar2;
  undefined8 uVar3;
  undefined8 uVar4;
  bool bVar5;
  undefined1 *puVar6;
  ulong uVar7;
  undefined8 *puVar8;
  ulong uVar9;
  undefined8 *puVar10;
  long lVar11;
  undefined8 uVar12;
  undefined8 uVar13;
  undefined8 uVar14;
  undefined8 uVar15;
  
  if (param_1 == param_2) {
    return;
  }
  if (((((ulong)param_1 & 7) == 0) && (((ulong)param_2 & 7) == 0)) || (*DAT_00110cc0 != '\0')) {
    if ((ulong)((long)param_1 - (long)param_2) < param_3) {
      puVar10 = (undefined8 *)((long)param_1 + param_3);
      param_2 = (undefined8 *)((long)param_2 + param_3);
      if (0x3f < param_3) {
        uVar2 = param_2[-1];
        uVar1 = param_2[-4];
        uVar3 = param_2[-3];
        uVar9 = (ulong)((long)puVar10 + -1) & 0xffffffffffffffe0;
        lVar11 = (long)puVar10 - uVar9;
        uVar12 = *(undefined8 *)((long)param_2 + (-0x10 - lVar11));
        uVar13 = *(undefined8 *)((long)param_2 + (-8 - lVar11));
        uVar14 = *(undefined8 *)((long)param_2 + (-0x20 - lVar11));
        uVar15 = *(undefined8 *)((long)param_2 + (-0x18 - lVar11));
        puVar10[-2] = param_2[-2];
        puVar10[-1] = uVar2;
        puVar10[-4] = uVar1;
        puVar10[-3] = uVar3;
        puVar6 = (undefined1 *)((long)param_2 + (-0x20 - lVar11));
        uVar7 = (param_3 - lVar11) - 0x40;
        if (0x3f < param_3 - lVar11 && uVar7 != 0) {
          do {
            *(undefined8 *)(uVar9 - 0x10) = uVar12;
            *(undefined8 *)(uVar9 - 8) = uVar13;
            *(undefined8 *)(uVar9 - 0x20) = uVar14;
            *(undefined8 *)(uVar9 - 0x18) = uVar15;
            uVar9 = uVar9 - 0x20;
            uVar12 = *(undefined8 *)(puVar6 + -0x10);
            uVar13 = *(undefined8 *)(puVar6 + -8);
            uVar14 = *(undefined8 *)(puVar6 + -0x20);
            uVar15 = *(undefined8 *)(puVar6 + -0x18);
            puVar6 = puVar6 + -0x20;
            bVar5 = 0x1f < uVar7;
            uVar7 = uVar7 - 0x20;
          } while (bVar5 && uVar7 != 0);
        }
        uVar1 = *(undefined8 *)(puVar6 + (-0x10 - uVar7));
        uVar3 = *(undefined8 *)(puVar6 + (-8 - uVar7));
        uVar2 = *(undefined8 *)(puVar6 + (-0x20 - uVar7));
        uVar4 = *(undefined8 *)(puVar6 + (-0x18 - uVar7));
        *(undefined8 *)(uVar9 - 0x10) = uVar12;
        *(undefined8 *)(uVar9 - 8) = uVar13;
        *(undefined8 *)(uVar9 - 0x20) = uVar14;
        *(undefined8 *)(uVar9 - 0x18) = uVar15;
        param_1[2] = uVar1;
        param_1[3] = uVar3;
        *param_1 = uVar2;
        param_1[1] = uVar4;
        return;
      }
      while (7 < param_3) {
        param_2 = param_2 + -1;
        puVar10 = puVar10 + -1;
        *puVar10 = *param_2;
        param_3 = param_3 - 8;
      }
      if (param_3 == 0) {
        return;
      }
      goto LAB_00110e98;
    }
    if (0x3f < param_3) {
      puVar8 = (undefined8 *)((ulong)(param_1 + 4) & 0xffffffffffffffe0);
      uVar2 = param_2[1];
      uVar1 = param_2[2];
      uVar3 = param_2[3];
      puVar10 = (undefined8 *)((long)param_2 + ((long)puVar8 - (long)param_1));
      uVar12 = *puVar10;
      uVar13 = puVar10[1];
      uVar14 = puVar10[2];
      uVar15 = puVar10[3];
      puVar10 = puVar10 + 4;
      param_3 = param_3 - ((long)puVar8 - (long)param_1);
      *param_1 = *param_2;
      param_1[1] = uVar2;
      param_1[2] = uVar1;
      param_1[3] = uVar3;
      uVar7 = param_3 - 0x40;
      if (0x3f < param_3 && uVar7 != 0) {
        do {
          *puVar8 = uVar12;
          puVar8[1] = uVar13;
          puVar8[2] = uVar14;
          puVar8[3] = uVar15;
          puVar8 = puVar8 + 4;
          uVar12 = *puVar10;
          uVar13 = puVar10[1];
          uVar14 = puVar10[2];
          uVar15 = puVar10[3];
          puVar10 = puVar10 + 4;
          bVar5 = 0x1f < uVar7;
          uVar7 = uVar7 - 0x20;
        } while (bVar5 && uVar7 != 0);
      }
      puVar10 = (undefined8 *)((long)puVar10 + uVar7);
      uVar1 = *puVar10;
      uVar3 = puVar10[1];
      uVar2 = puVar10[2];
      uVar4 = puVar10[3];
      *puVar8 = uVar12;
      puVar8[1] = uVar13;
      puVar8[2] = uVar14;
      puVar8[3] = uVar15;
      *(undefined8 *)((long)puVar8 + uVar7 + 0x20) = uVar1;
      *(undefined8 *)((long)puVar8 + uVar7 + 0x28) = uVar3;
      *(undefined8 *)((long)puVar8 + uVar7 + 0x30) = uVar2;
      *(undefined8 *)((long)puVar8 + uVar7 + 0x38) = uVar4;
      return;
    }
    while (7 < param_3) {
      *param_1 = *param_2;
      param_2 = param_2 + 1;
      param_3 = param_3 - 8;
      param_1 = param_1 + 1;
    }
    if (param_3 == 0) {
      return;
    }
  }
  else if ((ulong)((long)param_1 - (long)param_2) < param_3) {
    puVar10 = (undefined8 *)((long)param_1 + param_3);
    param_2 = (undefined8 *)((long)param_2 + param_3);
LAB_00110e98:
    do {
      param_2 = (undefined8 *)((long)param_2 + -1);
      puVar10 = (undefined8 *)((long)puVar10 + -1);
      *(undefined1 *)puVar10 = *(undefined1 *)param_2;
      param_3 = param_3 - 1;
    } while (param_3 != 0);
    return;
  }
  do {
    *(undefined1 *)param_1 = *(undefined1 *)param_2;
    param_3 = param_3 - 1;
    param_2 = (undefined8 *)((long)param_2 + 1);
    param_1 = (undefined8 *)((long)param_1 + 1);
  } while (param_3 != 0);
  return;
}


// ===== 0x00126494 -> FUN_00126494 @ 00126494

void FUN_00126494(undefined8 param_1,undefined8 param_2,ulong param_3)

{
  code *pcVar1;
  undefined8 uVar2;
  ulong uVar3;
  ulong unaff_x30;
  undefined1 auVar4 [16];
  
  uVar2 = FUN_0012c8c0(0);
  thunk_FUN_0012c678(uVar2,0x70);
  auVar4 = FUN_0012697c();
  uVar3 = auVar4._0_8_;
  if (uVar3 < auVar4._8_8_ || param_3 <= uVar3) {
                    /* WARNING: Subroutine does not return */
    FUN_0012ea7c();
  }
  FUN_001269a0(uVar3,uVar3,uVar3 + 0x60,0x70029e40);
  FUN_00126218();
  FUN_00126a0c();
  FUN_001269a0();
  FUN_00126ad8();
  FUN_00126a0c();
  if (((unaff_x30 ^ unaff_x30 << 1) >> 0x3e & 1) != 0) {
                    /* WARNING: Does not return */
    pcVar1 = (code *)SoftwareBreakpoint(0xc471,0x1265f4);
    (*pcVar1)();
  }
  FUN_00126988();
  return;
}



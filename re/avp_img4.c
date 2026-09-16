// ===== 0x00100984 -> FUN_00100984 @ 00100984

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_00100984(void)

{
  long lVar1;
  undefined1 uVar2;
  int iVar3;
  undefined8 uVar4;
  ulong in_x4;
  undefined4 *in_x5;
  undefined4 *in_x6;
  undefined4 *in_x7;
  ulong uVar5;
  ulong uVar6;
  long *in_stack_00000008;
  long *in_stack_00000010;
  long *in_stack_00000018;
  undefined4 local_7c;
  ulong local_78 [5];
  ulong uStack_50;
  undefined8 local_48;
  
  local_48 = _DAT_7002add8;
  local_78[2] = 0;
  local_78[3] = 0;
  local_78[0] = 0;
  local_78[1] = 0;
  uVar2 = in_x4 == 0x1e;
  if (0x1d < in_x4) {
    local_78[4] = FUN_00100dc0();
    uStack_50 = in_x4;
    uVar4 = FUN_00100dcc();
    iVar3 = FUN_00100b94(uVar4,0x2000000000000010);
    if (iVar3 == 0) {
      uVar5 = local_78[2] - local_78[4];
      lVar1 = uVar5 + local_78[0];
      uVar2 = lVar1 == 0;
      uVar6 = (long)uVar5 >> 0x3f;
      if (CARRY8(uVar5,local_78[0])) {
        uVar6 = uVar6 + 1;
      }
      uVar4 = 0xffffffff;
      if ((-(uVar6 & 1) != uVar6) || ((long)-(uVar6 & 1) < 0)) goto LAB_001009fc;
      FUN_00100de0(0xffffffff);
      iVar3 = FUN_00100bf4();
      if (iVar3 == 0) {
        FUN_00100de0();
        iVar3 = FUN_00100c78();
        if (iVar3 == 0) {
          uVar4 = FUN_00100dcc();
          iVar3 = FUN_00100b94(uVar4,0x2000000000000010);
          if (iVar3 == 0) {
            FUN_00100de0();
            iVar3 = FUN_00100bf4();
            if (iVar3 == 0) {
              FUN_00100de0();
              iVar3 = FUN_00100c78();
              if (iVar3 == 0) {
                uVar4 = FUN_00100dcc();
                iVar3 = FUN_00100b94(uVar4,0x16);
                uVar4 = 0xffffffff;
                if ((iVar3 != 0) || (uVar2 = local_78[3] == 4, !(bool)uVar2)) goto LAB_001009fc;
                if (in_x5 != (undefined4 *)0x0) {
                  local_7c = 0;
                  FUN_00111154(&local_7c,&local_7c,local_78,&PTR_LOOP_0013ce48,local_78[2],
                               local_78[2],local_78[2] + 4,&PTR_LOOP_0013ce88,4);
                  uVar4 = thunk_FUN_0010eecc(local_7c);
                  uVar2 = in_x5 >= in_x6 && in_x5 == in_x7;
                  if (in_x5 < in_x6 || in_x7 <= in_x5) goto LAB_00100b90;
                  *in_x5 = (int)uVar4;
                }
                if (in_stack_00000008 == (long *)0x0) {
                  uVar4 = 0;
                }
                else {
                  uVar2 = in_stack_00000008 >= in_stack_00000010 &&
                          in_stack_00000008 == in_stack_00000018;
                  if (in_stack_00000008 < in_stack_00000010 ||
                      in_stack_00000018 <= in_stack_00000008) {
LAB_00100b90:
                    /* WARNING: Subroutine does not return */
                    FUN_0012ea7c(uVar4);
                  }
                  uVar4 = 0;
                  *in_stack_00000008 = lVar1;
                }
                goto LAB_001009fc;
              }
            }
          }
        }
      }
    }
  }
  uVar4 = 0xffffffff;
LAB_001009fc:
  FUN_00100df0(local_48,uVar4);
  if ((bool)uVar2) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00123c18();
}


// ===== 0x0010746c -> FUN_0010746c @ 0010746c

undefined8 FUN_0010746c(undefined8 param_1,undefined8 param_2,undefined8 param_3,undefined8 param_4)

{
  int iVar1;
  undefined8 uVar2;
  
  uVar2 = FUN_0012c8c0(0);
  thunk_FUN_0012c6d8(uVar2,1,0x200,0x40);
  FUN_00107990();
  iVar1 = FUN_001262f8(param_1,param_2,param_3,param_4);
  uVar2 = 0;
  if (iVar1 == 0x200) {
    FUN_0010794c();
    uVar2 = FUN_00100e04();
  }
  FUN_0010794c();
  FUN_0010eee8();
  FUN_0010794c();
  FUN_001184fc();
  return uVar2;
}


// ===== 0x001010d0 -> FUN_001010d0 @ 001010d0

void FUN_001010d0(int param_1)

{
  undefined1 *puVar1;
  undefined1 *puVar2;
  undefined8 *puVar3;
  undefined8 *puVar4;
  undefined8 *puVar5;
  undefined8 *puVar6;
  undefined1 *puVar7;
  undefined1 *puVar8;
  undefined1 *puVar9;
  undefined1 auVar10 [16];
  
  puVar5 = (undefined8 *)&DAT_700284b0;
  puVar3 = (undefined8 *)&DAT_700284c8;
  puVar6 = (undefined8 *)&DAT_700284c0;
  puVar4 = (undefined8 *)&DAT_700284b8;
  while( true ) {
    puVar7 = (undefined1 *)*puVar5;
    if (puVar7 == &DAT_70028490) {
      return;
    }
    puVar8 = (undefined1 *)*puVar6;
    puVar9 = (undefined1 *)*puVar4;
    puVar2 = puVar8;
    auVar10 = FUN_00102ab4(puVar7,puVar9,puVar8,*puVar3);
    puVar1 = auVar10._0_8_;
    if (puVar1 < auVar10._8_8_ || puVar2 <= puVar1) break;
    if (*(int *)(puVar1 + 0x6c) == param_1) {
      return;
    }
    if (puVar7 < puVar9 || puVar8 <= puVar7) break;
    puVar5 = (undefined8 *)(puVar7 + 0x20);
    puVar4 = (undefined8 *)(puVar7 + 0x28);
    puVar6 = (undefined8 *)(puVar7 + 0x30);
    puVar3 = (undefined8 *)(puVar7 + 0x38);
  }
                    /* WARNING: Subroutine does not return */
  FUN_0012ea7c();
}


// ===== 0x001077c8 -> FUN_001077c8 @ 001077c8

void FUN_001077c8(undefined8 param_1,undefined8 param_2,undefined8 param_3,undefined8 param_4,
                 undefined8 param_5,undefined4 param_6)

{
  undefined1 uVar1;
  int iVar2;
  undefined8 uVar3;
  undefined8 extraout_x8;
  undefined4 *unaff_x19;
  undefined4 *unaff_x20;
  undefined4 *unaff_x21;
  undefined4 local_6c;
  undefined8 local_68;
  
  FUN_00107974();
  local_68 = extraout_x8;
  uVar3 = FUN_0012c8c0(0);
  thunk_FUN_0012c768(uVar3,0x70028f28);
  FUN_00107940();
  FUN_00107990();
  FUN_001113a0();
  uVar1 = unaff_x19 >= unaff_x20 && unaff_x19 == unaff_x21;
  if (unaff_x19 < unaff_x20 || unaff_x21 <= unaff_x19) {
                    /* WARNING: Subroutine does not return */
    FUN_0012ea7c();
  }
  *unaff_x19 = (int)param_5;
  unaff_x19[2] = 0x4d656d7a;
  unaff_x19[3] = param_6;
  *(undefined8 *)(unaff_x19 + 4) = param_1;
  *(undefined8 *)(unaff_x19 + 6) = param_2;
  *(undefined8 *)(unaff_x19 + 8) = param_3;
  *(undefined8 *)(unaff_x19 + 10) = param_4;
  local_6c = 0;
  iVar2 = FUN_00100984(param_1,param_2,param_3,param_4,param_5,&local_6c,&local_6c,&local_68,
                       &PTR_LOOP_0013ce48,0,0,0,0);
  if (iVar2 == 0) {
    unaff_x19[1] = local_6c;
  }
  else {
    FUN_0010794c();
    FUN_001184fc();
  }
  FUN_00107960(local_68);
  if ((bool)uVar1) {
    FUN_0010794c();
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00123c18();
}



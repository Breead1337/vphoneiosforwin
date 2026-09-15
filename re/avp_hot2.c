// ===== 0x139afc -> FUN_001399c0 @ 001399c0

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_001399c0(ulong *param_1,long param_2,long param_3)

{
  long lVar1;
  uint *puVar2;
  uint uVar3;
  long lVar4;
  bool bVar5;
  long extraout_x8;
  ulong uVar6;
  ulong uVar7;
  ulong uVar8;
  ulong *puVar9;
  ulong uStack_60;
  ulong local_58;
  
  local_58 = _DAT_7002add8;
  uVar7 = param_1[1];
  uVar8 = param_1[2];
  lVar1 = param_2 + uVar7 + 8;
  if (uVar8 <= *(uint *)(lVar1 + uVar8)) {
    *(undefined4 *)(lVar1 + uVar8) = 0;
  }
  lVar1 = uVar7 + 8;
  (*(code *)PTR_FUN_001476a0)((lVar1 + uVar8 + 0xb & 0xfffffffffffffff8) + 0xf & 0xfffffffffffffff0)
  ;
  lVar4 = -extraout_x8;
  puVar9 = (ulong *)((long)&uStack_60 + lVar4);
  FUN_00110ed0(puVar9);
  FUN_00110cf0(puVar9,param_2,lVar1 + uVar8 + 4);
  uVar3 = *(uint *)((long)puVar9 + uVar8 + lVar1);
  *puVar9 = *puVar9 + (ulong)(uVar3 << 3);
  *(uint *)((long)puVar9 + uVar8 + lVar1) = uVar3 + 1;
  *(undefined1 *)((long)puVar9 + (ulong)uVar3 + lVar1) = 0x80;
  uVar6 = (ulong)*(uint *)((long)puVar9 + uVar8 + lVar1);
  if (uVar8 - 0x10 < uVar6) {
    while (uVar6 < uVar8) {
      *(int *)((long)puVar9 + uVar8 + lVar1) = (int)uVar6 + 1;
      *(undefined1 *)((long)puVar9 + uVar6 + lVar1) = 0;
      uVar6 = (ulong)*(uint *)((long)puVar9 + uVar8 + lVar1);
    }
    (*(code *)param_1[6])((long)&local_58 + lVar4,1);
    uVar6 = 0;
    uVar7 = param_1[1];
    uVar8 = param_1[2];
    *(undefined4 *)((long)puVar9 + uVar8 + uVar7 + 8) = 0;
  }
  puVar2 = (uint *)((long)puVar9 + uVar8 + uVar7 + 8);
  while (uVar6 < uVar8 - 8) {
    *puVar2 = (int)uVar6 + 1;
    *(undefined1 *)((long)puVar9 + uVar6 + uVar7 + 8) = 0;
    uVar6 = (ulong)*puVar2;
  }
  uVar7 = (*puVar9 & 0xff00ff00ff00ff00) >> 8 | (*puVar9 & 0xff00ff00ff00ff) << 8;
  uVar7 = (uVar7 & 0xffff0000ffff0000) >> 0x10 | (uVar7 & 0xffff0000ffff) << 0x10;
  *(ulong *)(puVar2 + -2) = uVar7 >> 0x20 | uVar7 << 0x20;
  (*(code *)param_1[6])((long)&local_58 + lVar4,1);
  if (7 < *param_1) {
    uVar6 = 0;
    uVar7 = 0;
    uVar8 = 1;
    do {
      uVar7 = *(ulong *)((long)&local_58 + lVar4 + uVar7 * 8);
      uVar7 = (uVar7 & 0xff00ff00ff00ff00) >> 8 | (uVar7 & 0xff00ff00ff00ff) << 8;
      uVar7 = (uVar7 & 0xffff0000ffff0000) >> 0x10 | (uVar7 & 0xffff0000ffff) << 0x10;
      *(ulong *)(param_3 + uVar6) = uVar7 >> 0x20 | uVar7 << 0x20;
      uVar6 = (ulong)((int)uVar6 + 8);
      bVar5 = uVar8 < *param_1 >> 3;
      uVar7 = uVar8;
      uVar8 = (ulong)((int)uVar8 + 1);
    } while (bVar5);
  }
  FUN_00138bac(param_1[1] + param_1[2] + 0xc,puVar9);
  if (_DAT_7002add8 == local_58) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00123c18();
}


// ===== 0x110974 -> FUN_001108e8 @ 001108e8

long FUN_001108e8(long param_1,char *param_2,char *param_3,undefined8 param_4,long param_5,
                 char *param_6,char *param_7,undefined8 param_8,ulong param_9)

{
  char *pcVar1;
  char *pcVar2;
  ulong uVar3;
  long lVar4;
  long lVar5;
  
  uVar3 = FUN_00110b98();
  if (param_9 == 0 || param_9 == uVar3) {
    lVar4 = FUN_00110ac4(param_5,param_6,param_7,param_8);
    lVar4 = lVar4 + uVar3;
  }
  else {
    for (lVar4 = 0; lVar5 = param_9 + ~uVar3, param_9 + ~uVar3 != lVar4; lVar4 = lVar4 + 1) {
      pcVar1 = (char *)(param_5 + lVar4);
      if (pcVar1 < param_6 || param_7 <= pcVar1) goto LAB_001109f8;
      lVar5 = lVar4;
      if (*pcVar1 == '\0') break;
      pcVar2 = (char *)(param_1 + uVar3 + lVar4);
      if (pcVar2 < param_2 || param_3 <= pcVar2) goto LAB_001109f8;
      *pcVar2 = *pcVar1;
    }
    pcVar1 = (char *)(param_1 + uVar3 + lVar5);
    if (pcVar1 < param_2 || param_3 <= pcVar1) {
LAB_001109f8:
                    /* WARNING: Subroutine does not return */
      FUN_0012ea7c();
    }
    *pcVar1 = '\0';
    lVar4 = FUN_00110ac4(param_5 + lVar5,param_6,param_7,param_8);
    lVar4 = lVar5 + uVar3 + lVar4;
  }
  return lVar4;
}



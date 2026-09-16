// ===== 0x00104bbc -> FUN_00104bbc @ 00104bbc

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_00104bbc(byte param_1,undefined8 param_2,undefined8 param_3,undefined8 param_4)

{
  int iVar1;
  long lVar2;
  undefined8 uVar3;
  undefined1 auVar4 [16];
  undefined1 auStack_70 [32];
  undefined4 local_50;
  undefined4 uStack_4c;
  long local_48;
  
  local_48 = _DAT_7002add8;
  uVar3 = 0x28;
  FUN_00110cf0(auStack_70,s_firmware_00142010,0x28);
  FUN_00104d1c(&DAT_0014673b);
  auVar4 = thunk_FUN_00124804();
  if (auVar4._0_8_ != 0) {
    iVar1 = FUN_00110b2c(auStack_70,auStack_70,&local_50,0x70028700,s_pmusram_00146740,
                         s_pmusram_00146740,&DAT_00146748,&PTR_LOOP_0013ce88,0x20);
    if (((param_1 ^ iVar1 == 0) & 1) == 0) {
      lVar2 = thunk_FUN_00126a58(s_virt_firmware_00146680,s_virt_firmware_00146680,&DAT_0014668e,
                                 &PTR_LOOP_0013ce88,auVar4._0_8_,auVar4._8_8_,uVar3,param_4,local_50
                                 ,uStack_4c,1);
      if (lVar2 != 0) {
        FUN_00126214();
      }
    }
  }
  if (_DAT_7002add8 == local_48) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00123c18();
}


// ===== 0x001004b8 -> FUN_001004b8 @ 001004b8

void FUN_001004b8(void)

{
  uint *puVar1;
  undefined4 uVar2;
  bool bVar3;
  uint uVar4;
  undefined4 uVar5;
  bool bVar6;
  bool bVar7;
  int iVar8;
  ulong uVar9;
  undefined8 uVar10;
  undefined8 uVar11;
  uint *puVar12;
  int iVar13;
  uint *puVar14;
  uint *puVar15;
  ulong uVar16;
  uint uVar17;
  undefined1 auVar18 [16];
  undefined4 uVar19;
  undefined **local_88;
  undefined4 local_78;
  undefined4 local_74;
  int iStack_70;
  undefined4 local_6c;
  undefined1 auStack_68 [8];
  
  local_74 = 0;
  iStack_70 = 0;
  local_78 = 0;
  FUN_00124174();
  FUN_00104254();
  FUN_001109fc(0x7002ab40,0x7002ab40,&DAT_7002ab90,&PTR_LOOP_0013ce88,s_mBoot_18000_161_10_00100280,
               s_mBoot_18000_161_10_00100280,&PTR_DAT_00100300,&PTR_LOOP_0013ce88,0x4f);
  FUN_001043ac();
  FUN_00104358();
  DAT_7002ae28 = FUN_00104738();
  thunk_FUN_00104cf8(0);
  FUN_001042b4();
  FUN_00105948();
  FUN_00103234(1);
  FUN_00103234(2);
  FUN_00103234(4);
  FUN_00103234(8);
  FUN_00103234(0x10);
  CallSupervisor(10);
  FUN_00105aec(2);
  FUN_001042bc(1);
  FUN_00104580();
  uVar17 = 0;
  if (DAT_7002ae28 == '\x01') {
    FUN_0010420c(0x20001);
    uVar17 = 0xffffffff;
  }
  do {
    uVar19 = 0;
    uVar9 = FUN_001045d0(uVar17,&iStack_70,&iStack_70,&local_6c,&PTR_LOOP_0013ce48,&local_74,
                         &local_74,&iStack_70,&PTR_LOOP_0013ce48,&local_78,&local_78,&local_74,
                         &PTR_LOOP_0013ce48);
    if ((uVar9 & 1) == 0) {
      uVar19 = 0x80020003;
LAB_00100928:
      FUN_0010420c(uVar19);
      FUN_001045bc(0);
LAB_00100934:
      FUN_00108cb4();
      FUN_00105f80();
LAB_0010093c:
      FUN_001060c0();
      FUN_00105374(0,0x70074000,0);
LAB_00100954:
                    /* WARNING: Subroutine does not return */
      FUN_0012ea7c();
    }
    FUN_00105b48(1);
    iVar13 = iStack_70;
    uVar2 = local_74;
    uVar5 = local_78;
    uVar10 = FUN_00123d70();
    uVar9 = FUN_001040cc();
    puVar1 = (uint *)(uVar9 + 0x70074000);
    FUN_00104678(1,iVar13,uVar5);
    if (iVar13 == 6) {
      thunk_FUN_00104a90();
      FUN_0010472c(1);
      thunk_FUN_00104cf8(1);
      uVar10 = FUN_00123d7c();
      FUN_00104214(0x20009,6,uVar2,uVar5);
      uVar16 = FUN_00126fa8(0x70074000,0x70074000,puVar1,&PTR_LOOP_0013ce88,uVar9,1);
      uVar2 = 0x4002000a;
      if (-1 < (int)uVar16) {
        uVar2 = 0x2000a;
      }
      FUN_00104214(uVar2,uVar16,0,0);
      FUN_0010472c(0);
      if (-1 < (int)uVar16) {
        if (uVar9 < (uVar16 & 0xffffffff)) {
          iVar13 = 6;
          goto LAB_00100978;
        }
        local_88 = &PTR_LOOP_0013ce88;
        puVar15 = puVar1;
        auVar18 = FUN_001077c8(0x70074000,0x70074000,puVar1,&PTR_LOOP_0013ce88,uVar16 & 0xffffffff,0
                              );
        if (auVar18._0_8_ != 0) goto LAB_00100780;
        FUN_0010420c(0x40030006);
      }
LAB_001008a4:
      bVar7 = false;
      bVar6 = false;
    }
    else {
      if (iVar13 != 0xe) goto LAB_001008a4;
      puVar15 = (uint *)&DAT_0014668e;
      local_88 = &PTR_LOOP_0013ce88;
      auVar18 = thunk_FUN_00124804(s_virt_firmware_00146680,s_virt_firmware_00146680);
      if (auVar18._0_8_ == 0) goto LAB_001008a4;
      uVar11 = FUN_001242ac();
      iVar8 = FUN_0010746c(auVar18._0_8_,auVar18._8_8_,puVar15,local_88,uVar11,4);
      if ((iVar8 == 0) || (auVar18 = thunk_FUN_001010d0(uVar10), auVar18._0_8_ == 0))
      goto LAB_001008a4;
LAB_00100780:
      puVar14 = auVar18._8_8_;
      puVar12 = auVar18._0_8_;
      if (puVar12 < puVar14 || puVar15 <= puVar12) goto LAB_00100954;
      uVar16 = (ulong)*puVar12;
      if (uVar9 < uVar16) {
LAB_00100978:
        FUN_00104214(0x80030005,iVar13,uVar16,uVar9);
                    /* WARNING: Subroutine does not return */
        FUN_0010550c();
      }
      bVar6 = (puVar12[3] & 4) == 0;
      local_6c = (undefined4)uVar10;
      uVar4 = puVar12[3] | 0xb;
      puVar12[3] = uVar4;
      FUN_00104214(0x30009,uVar10,uVar4,0);
      uVar10 = FUN_00107568(puVar12,puVar14,puVar15,local_88,&local_6c,&local_6c,auStack_68,
                            &PTR_LOOP_0013ce48,CONCAT44(uVar19,1),0,0,0,0,0x70074000,0x70074000,
                            puVar1,&PTR_LOOP_0013ce88,uVar9,0,0,0,0,0,0,0,0,0,0);
      bVar7 = (int)uVar10 == 0;
      if ((int)uVar10 == 0) {
        FUN_0010420c(0x3000a);
      }
      else {
        FUN_00104214(0x4003000b,uVar10,0,0);
      }
      FUN_001078f8(puVar12,puVar14,puVar15,local_88);
    }
    iVar8 = thunk_FUN_00123d30();
    if (iVar8 != 0) {
      bVar3 = bVar7;
      if (iVar13 != 6) {
        bVar3 = true;
      }
      if (!bVar3) {
        uVar19 = 0x80020014;
        goto LAB_00100928;
      }
      FUN_0010420c(0x20015);
    }
    FUN_00104678(0,iVar13,uVar5);
    if (bVar7) {
      FUN_0010420c(0x2000b);
      if (!bVar6) goto LAB_00100934;
      FUN_00105f80();
      FUN_00104340();
      goto LAB_0010093c;
    }
    uVar17 = uVar17 - ((int)~uVar17 >> 0x1f);
  } while( true );
}


// ===== 0x0010829c -> FUN_0010829c @ 0010829c

undefined8 FUN_0010829c(void)

{
  uint uVar1;
  byte *pbVar2;
  ulong uVar3;
  uint *puVar4;
  long *plVar5;
  long lVar6;
  long *plVar7;
  long lVar8;
  long lVar9;
  byte *pbVar10;
  char cVar11;
  int iVar12;
  ulong uVar13;
  code *extraout_x8;
  code *extraout_x8_00;
  byte *pbVar14;
  undefined8 uVar15;
  long *plVar16;
  
  pbVar10 = DAT_001476b0;
  do {
    do {
      FUN_001239ac();
      if (pbVar10[2] == 0) {
        return 0;
      }
      uVar3 = *(ulong *)(pbVar10 + 0x70);
      if (uVar3 < *(ulong *)(pbVar10 + 0x78) || *(ulong *)(pbVar10 + 0x80) <= uVar3)
      goto LAB_0010860c;
      iVar12 = FUN_0010dc5c(uVar3,uVar3,uVar3 + 0x60,0x700290a8,0);
    } while (iVar12 == 0);
    FUN_001185a8();
    puVar4 = *(uint **)(pbVar10 + 0x10);
    if (puVar4 < *(uint **)(pbVar10 + 0x18) || *(uint **)(pbVar10 + 0x20) <= puVar4)
    goto LAB_0010860c;
    if ((0xfffffff9 < *puVar4) || (uVar1 = *puVar4 + 6, *(uint *)(pbVar10 + 4) < uVar1)) {
LAB_00108608:
                    /* WARNING: Subroutine does not return */
      FUN_0010550c();
    }
    FUN_001113a0(*(undefined8 *)(pbVar10 + 0x50),*(undefined8 *)(pbVar10 + 0x58),
                 *(undefined8 *)(pbVar10 + 0x60),*(undefined8 *)(pbVar10 + 0x68),0);
    FUN_00111154(*(undefined8 *)(pbVar10 + 0x50),*(undefined8 *)(pbVar10 + 0x58),
                 *(undefined8 *)(pbVar10 + 0x60),*(undefined8 *)(pbVar10 + 0x68),
                 *(undefined8 *)(pbVar10 + 0x10),*(undefined8 *)(pbVar10 + 0x18),
                 *(undefined8 *)(pbVar10 + 0x20),*(undefined8 *)(pbVar10 + 0x28),uVar1);
    FUN_00108200();
    uVar3 = *(ulong *)(pbVar10 + 0x50);
    if (uVar3 < *(ulong *)(pbVar10 + 0x58) || *(ulong *)(pbVar10 + 0x60) <= uVar3)
    goto LAB_0010860c;
    cVar11 = *(char *)(uVar3 + 5);
    if (cVar11 == '\x03') {
      if (((*pbVar10 & 1) != 0) &&
         (((cVar11 = *(char *)(uVar3 + 4), cVar11 == '\x02' || cVar11 == '\x04' || (cVar11 == -0x7b)
           ) || (cVar11 == -0x7f)))) {
        iVar12 = FUN_00108a10();
        uVar13 = (ulong)(uint)(iVar12 << 3 | iVar12 << 6);
        pbVar14 = pbVar10 + 0xb0;
        pbVar2 = pbVar14 + uVar13;
        if (CARRY8(uVar13,(ulong)pbVar14)) {
LAB_00108614:
                    /* WARNING: Subroutine does not return */
          FUN_0012e910();
        }
        if (pbVar2 < pbVar14 || pbVar10 + 0x1d0 <= pbVar2) goto LAB_0010860c;
        if (*(short *)(pbVar2 + 2) != 0) {
          pbVar2[2] = 0;
          pbVar2[3] = 0;
          pbVar14 = pbVar2 + 8;
          while (plVar16 = *(long **)pbVar14, plVar16 != (long *)0x0) {
            plVar5 = *(long **)(pbVar2 + 0x10);
            plVar7 = *(long **)(pbVar2 + 0x18);
            if (plVar16 < plVar5 || plVar7 <= plVar16) goto LAB_0010860c;
            uVar15 = *(undefined8 *)(pbVar2 + 0x20);
            lVar6 = *plVar16;
            lVar8 = plVar16[1];
            lVar9 = plVar16[3];
            *(long *)(pbVar2 + 0x18) = plVar16[2];
            *(long *)(pbVar2 + 0x20) = lVar9;
            *(long *)pbVar14 = lVar6;
            *(long *)(pbVar2 + 0x10) = lVar8;
            if (lVar6 == 0) {
              *(byte **)(pbVar2 + 0x28) = pbVar14;
              *(byte **)(pbVar2 + 0x30) = pbVar14;
              *(byte **)(pbVar2 + 0x38) = pbVar2 + 0x28;
              pbVar2[0x40] = 0x90;
              pbVar2[0x41] = 0x90;
              pbVar2[0x42] = 2;
              pbVar2[0x43] = 0x70;
              pbVar2[0x44] = 0;
              pbVar2[0x45] = 0;
              pbVar2[0x46] = 0;
              pbVar2[0x47] = 0;
            }
            FUN_001184fc(plVar16[5],plVar16[6],plVar16[7],plVar16[8]);
            plVar16[7] = 0;
            plVar16[8] = 0;
            plVar16[5] = 0;
            plVar16[6] = 0;
            FUN_001184fc(plVar16,plVar5,plVar7,uVar15);
          }
        }
      }
      cVar11 = *(char *)(uVar3 + 4);
      uVar15 = 5;
LAB_001085d8:
      FUN_0010871c(cVar11,uVar15);
    }
    else if (cVar11 == '\x02') {
      FUN_0010871c(*(undefined1 *)(uVar3 + 4),4);
      uVar3 = *(ulong *)(pbVar10 + 0x70);
      if (uVar3 < *(ulong *)(pbVar10 + 0x78) || *(ulong *)(pbVar10 + 0x80) <= uVar3)
      goto LAB_0010860c;
      if (*(long *)(uVar3 + 0x60) == 0) goto LAB_00108610;
      FUN_00108d3c();
      (*extraout_x8)();
    }
    else {
      if (cVar11 != '\x01') goto LAB_00108608;
      if (((*pbVar10 & 1) != 0) &&
         (((cVar11 = *(char *)(uVar3 + 4), cVar11 == '\x02' || cVar11 == '\x04' || (cVar11 == -0x7b)
           ) || (cVar11 == -0x7f)))) {
        iVar12 = FUN_00108a10();
        uVar13 = (ulong)(uint)(iVar12 << 3 | iVar12 << 6);
        pbVar14 = pbVar10 + 0xb0;
        pbVar2 = pbVar14 + uVar13;
        if (CARRY8(uVar13,(ulong)pbVar14)) goto LAB_00108614;
        if (pbVar2 < pbVar14 || pbVar10 + 0x1d0 <= pbVar2) goto LAB_0010860c;
        pbVar14 = pbVar2 + 8;
        plVar16 = *(long **)pbVar14;
        if (plVar16 != (long *)0x0) {
          plVar5 = *(long **)(pbVar2 + 0x10);
          plVar7 = *(long **)(pbVar2 + 0x18);
          if (plVar16 < plVar5 || plVar7 <= plVar16) goto LAB_0010860c;
          uVar15 = *(undefined8 *)(pbVar2 + 0x20);
          lVar6 = *plVar16;
          lVar8 = plVar16[1];
          lVar9 = plVar16[3];
          *(long *)(pbVar2 + 0x18) = plVar16[2];
          *(long *)(pbVar2 + 0x20) = lVar9;
          *(long *)pbVar14 = lVar6;
          *(long *)(pbVar2 + 0x10) = lVar8;
          if (lVar6 == 0) {
            *(byte **)(pbVar2 + 0x28) = pbVar14;
            *(byte **)(pbVar2 + 0x30) = pbVar14;
            *(byte **)(pbVar2 + 0x38) = pbVar2 + 0x28;
            pbVar2[0x40] = 0x90;
            pbVar2[0x41] = 0x90;
            pbVar2[0x42] = 2;
            pbVar2[0x43] = 0x70;
            pbVar2[0x44] = 0;
            pbVar2[0x45] = 0;
            pbVar2[0x46] = 0;
            pbVar2[0x47] = 0;
          }
          FUN_00108a60(plVar16[5],plVar16[6],plVar16[7],plVar16[8],(int)plVar16[4],
                       *(undefined1 *)(uVar3 + 4));
          FUN_001184fc(plVar16[5],plVar16[6],plVar16[7],plVar16[8]);
          plVar16[7] = 0;
          plVar16[8] = 0;
          plVar16[5] = 0;
          plVar16[6] = 0;
          FUN_001184fc(plVar16,plVar5,plVar7,uVar15);
          goto LAB_001085dc;
        }
        *(short *)(pbVar2 + 2) = *(short *)(pbVar2 + 2) + 1;
      }
      uVar13 = *(ulong *)(pbVar10 + 0x70);
      if (uVar13 < *(ulong *)(pbVar10 + 0x78) || *(ulong *)(pbVar10 + 0x80) <= uVar13) {
LAB_0010860c:
                    /* WARNING: Subroutine does not return */
        FUN_0012ea7c();
      }
      if (*(long *)(uVar13 + 0x60) == 0) {
LAB_00108610:
                    /* WARNING: Subroutine does not return */
        FUN_0012e944();
      }
      FUN_00108d3c();
      (*extraout_x8_00)();
      if (((*pbVar10 & 1) != 0) &&
         (cVar11 = *(char *)(uVar3 + 4), cVar11 == '\x04' || cVar11 == '\x02')) {
        uVar15 = 1;
        goto LAB_001085d8;
      }
    }
LAB_001085dc:
    FUN_00118654();
  } while( true );
}


// ===== 0x0010d8c8 -> FUN_0010d8c8 @ 0010d8c8

undefined8 FUN_0010d8c8(void)

{
  undefined1 (*pauVar1) [16];
  undefined1 (*pauVar2) [16];
  int iVar3;
  long *plVar4;
  undefined8 uVar5;
  long lVar6;
  long lVar7;
  int in_w4;
  byte in_w5;
  ulong uVar8;
  long *unaff_x19;
  long *unaff_x20;
  ulong uVar9;
  undefined1 auVar10 [16];
  
  plVar4 = (long *)FUN_0010df10();
  uVar5 = FUN_0010dac0();
  if ((int)uVar5 == 1) {
    FUN_0010ded4();
    FUN_0010dae8();
    FUN_0010ded4();
    iVar3 = FUN_0010dac0();
    if (iVar3 == 1) {
      FUN_0010ded4();
      lVar7 = 4;
      iVar3 = FUN_0010dac0();
      if (iVar3 == in_w4) {
        if (unaff_x20 <= plVar4 && plVar4 < unaff_x19) {
          if (*(ulong *)(*plVar4 + 8) < 0x10000) {
            *(int *)(plVar4 + 1) = (int)*(ulong *)(*plVar4 + 8);
            if (in_w5 < 3) {
              uVar9 = 0;
              pauVar1 = (undefined1 (*) [16])(plVar4 + 2);
              while( true ) {
                if (((ulong)in_w5 * 4 + (ulong)in_w5) * 8 - uVar9 == 0) {
                  *(byte *)((long)plVar4 + 0xc) = in_w5;
                  *(undefined1 *)((long)plVar4 + 0xd) = 0;
                  if (in_w5 != 0) {
                    FUN_0010ded4();
                    FUN_0010dae8();
                  }
                  return 0;
                }
                pauVar2 = (undefined1 (*) [16])((long)*pauVar1 + uVar9);
                uVar8 = -(ulong)CARRY8((ulong)pauVar1,uVar9);
                if ((uVar8 != CARRY8((ulong)pauVar1,uVar9)) || ((long)uVar8 < 0)) {
                    /* WARNING: Subroutine does not return */
                  FUN_0012e910();
                }
                if (pauVar2 < pauVar1 || (undefined1 (*) [16])(plVar4 + 0xc) <= pauVar2) break;
                uVar5 = FUN_0012c8c0(0);
                lVar6 = 5;
                thunk_FUN_0012c6a8(uVar5,0x10);
                auVar10 = FUN_0010deb0();
                *pauVar2 = auVar10;
                *(long *)pauVar2[1] = lVar6;
                *(long *)((long)pauVar2[1] + 8) = lVar7;
                uVar9 = uVar9 + 0x28;
                *(undefined4 *)pauVar2[2] = 0;
              }
              goto LAB_0010dab8;
            }
            uVar5 = 0x32;
          }
          else {
            uVar5 = 0x2f;
          }
          FUN_0010debc(uVar5);
          FUN_0010def4();
        }
LAB_0010dab8:
                    /* WARNING: Subroutine does not return */
        FUN_0012ea7c();
      }
      FUN_0010debc(0x2a);
      FUN_0010df1c();
      FUN_001275ac(0x40200003);
      uVar5 = 0xfffffffd;
    }
    else {
      FUN_0010debc(0x24);
      FUN_0010df1c();
      FUN_001275ac(0x40200002);
      uVar5 = 0xfffffffe;
    }
  }
  else {
    FUN_0010debc(0x1d);
    FUN_0010df1c();
    FUN_00127704(0x40200001,uVar5);
    uVar5 = 0xffffffff;
  }
  return uVar5;
}



// ===== 0x7006f410 -> FUN_7006f410 @ 7006f410

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_7006f410(void)

{
  char *pcVar1;
  char *pcVar2;
  char *pcVar3;
  undefined *puVar4;
  undefined *puVar5;
  undefined *puVar6;
  undefined8 *puVar7;
  undefined8 uVar8;
  byte bVar9;
  int iVar10;
  int iVar11;
  uint uVar12;
  int iVar13;
  undefined4 uVar14;
  ulong uVar15;
  long lVar16;
  undefined8 uVar17;
  ulong uVar18;
  undefined **ppuVar19;
  undefined8 extraout_x1;
  undefined8 extraout_x1_00;
  undefined *puVar20;
  undefined **ppuVar21;
  undefined1 *puVar22;
  code *pcVar23;
  undefined8 uVar24;
  int unaff_w24;
  char **in_stack_fffffffffffffeb8;
  char *local_f0;
  char *pcStack_e8;
  char *local_e0;
  undefined1 *puStack_d8;
  undefined *local_d0;
  undefined *puStack_c8;
  char *local_c0;
  undefined1 *puStack_b8;
  undefined1 local_b0 [16];
  char *local_a0;
  undefined1 *puStack_98;
  undefined8 local_90;
  undefined8 uStack_88;
  undefined8 *local_80;
  undefined8 uStack_78;
  undefined4 local_70;
  undefined1 local_6c;
  undefined1 auStack_6b [11];
  
  FUN_700c1d50(0x3c4d5243,0);
  FUN_700c1d50(0x3c504653,0);
  FUN_70085d64();
  FUN_700c1d50(0x3e504653,0);
  FUN_7006c58c();
  FUN_700c1d50(0x3c4c6445,0);
  FUN_700711d8();
  FUN_700c1d50(0x3e4c6445,0);
  puVar22 = &LAB_70105fb8;
  FUN_700ad804(s_debug_uarts_701100cf,s_debug_uarts_701100cf,s_delay_recovery_image_701100db,
               &LAB_70105fb8,0);
  FUN_70089aec();
  FUN_700bf3cc(0);
  FUN_700c7378(0x2007b00);
  if ((DAT_70120f58 & 1) != 0) {
    FUN_700dcc1c(1);
  }
  thunk_FUN_7008bdc0();
  FUN_700704f0(0x4944);
  thunk_FUN_700dd5e8();
  FUN_700704d8(0x4944);
  uVar15 = FUN_70083c20();
  if ((uVar15 & 1) == 0) {
    FUN_700c1d50(0x3c577544,0);
    while( true ) {
      if ((_DAT_70120f70 == 0) || (iVar10 = FUN_700ddb1c(), iVar10 == 0)) goto LAB_7006f558;
      iVar10 = FUN_700e7db8(_DAT_70120f70,5000000);
      if (iVar10 != 0) break;
      FUN_700dc88c(10000);
    }
    _DAT_70120f68 = 0;
    FUN_700ddb78();
LAB_7006f558:
    FUN_700c1d50(0x3e577544,0);
  }
  FUN_700c1d50(0x3c625549,0);
  uVar15 = FUN_70083c20();
  if ((uVar15 & 1) == 0) {
    FUN_700bf1a0();
    FUN_700bf180();
  }
  FUN_700bcda8(0,0,0);
  FUN_70070498();
  FUN_700bce24(0x6c6f676f);
  FUN_700bdeb0();
  FUN_700c1d50(0x3e625549,0);
  FUN_700704f0(0x4944);
  thunk_FUN_700dd5e8();
  FUN_700704d8(0x4944);
  FUN_700dcc1c(0);
  uVar24 = 0x70120000;
  while ((_DAT_70120f60 != 0 && (iVar10 = thunk_FUN_7008bdc0(1), iVar10 != 0))) {
    iVar10 = FUN_700e7db8(_DAT_70120f60,5000000);
    if (iVar10 != 0) {
      FUN_70086a28();
      goto LAB_7006fa18;
    }
    FUN_700dc88c(10000);
  }
  FUN_700c1d50(0x3c504c49,0);
  FUN_70085b3c();
  FUN_700c1d50(0x3e504c49,0);
  thunk_FUN_700c6038();
  FUN_7008e158();
  iVar10 = FUN_70083c20();
  pcVar1 = s_Remote_70110143;
  if (iVar10 == 0) {
    pcVar1 = s_Local_7011014a;
  }
  local_80 = (undefined8 *)0x0;
  uStack_78 = 0;
  pcVar2 = s_Local_7011014a;
  if (iVar10 == 0) {
    pcVar2 = &DAT_70110150;
  }
  local_90 = (undefined8 *)0x0;
  uStack_88 = 0;
  FUN_700b85a4(0x2005900,0x60000,&local_90,&local_90,&local_70,&LAB_70105f90);
  uVar8 = uStack_78;
  puVar7 = local_80;
  uVar17 = uStack_88;
  uVar24 = local_90;
  iVar10 = thunk_FUN_70087ee4();
  pcVar3 = &DAT_70110150;
  if (iVar10 == 0) {
    pcVar3 = &DAT_70110154;
  }
  puVar4 = &DAT_70110154;
  if (iVar10 == 0) {
    puVar4 = &DAT_70110157;
  }
  iVar10 = FUN_700dcce0();
  local_6c = 0;
  local_70 = 0;
  puVar5 = &DAT_70110157;
  if (iVar10 == 0) {
    puVar5 = &DAT_7011015c;
  }
  local_80 = (undefined8 *)0x0;
  uStack_78 = 0;
  puVar6 = &DAT_7011015c;
  if (iVar10 == 0) {
    puVar6 = &DAT_70110161;
  }
  local_90 = (undefined8 *)0x0;
  uStack_88 = 0;
  puVar20 = &DAT_700cd020;
  FUN_700b4304(&DAT_700cd010,&DAT_700cd010,&DAT_700cd020,&LAB_70105fb8,&local_90,&local_90,
               auStack_6b,&LAB_70105fb8);
  FUN_700b2780(s__________________________________70110178);
  FUN_700b2780(&DAT_701101a3);
  local_b0._0_8_ = s_iBoot_for_vresearch101_Copyright_7006c200;
  local_b0._8_8_ = s_iBoot_for_vresearch101_Copyright_7006c200;
  local_a0 = s_RELEASE_7006c240;
  puStack_98 = &LAB_70105fb8;
  local_d0 = &DAT_70110161;
  puStack_c8 = &DAT_70110161;
  local_c0 = s_Microkernel_7011016b;
  puStack_b8 = &LAB_70105fb8;
  local_f0 = s_Microkernel_7011016b;
  pcStack_e8 = s_Microkernel_7011016b;
  local_e0 = s__________________________________70110178;
  puStack_d8 = &LAB_70105fb8;
  in_stack_fffffffffffffeb8 = &local_f0;
  FUN_700b2780(s_____s_s_s_701101a7);
  FUN_700b2780(&DAT_701101a3);
  thunk_FUN_70088520();
  FUN_700dccd0();
  puStack_98 = &LAB_70105fb8;
  local_d0 = (undefined *)uVar24;
  puStack_c8 = (undefined *)uVar17;
  local_c0 = (char *)puVar7;
  puStack_b8 = (undefined1 *)uVar8;
  puStack_d8 = &LAB_70105fb8;
  local_f0 = pcVar3;
  pcStack_e8 = pcVar3;
  local_e0 = puVar4;
  local_b0._0_8_ = pcVar1;
  local_b0._8_8_ = pcVar1;
  local_a0 = pcVar2;
  FUN_700b2780(s_____s_boot__Board_0x_x___s_s__Re_701101b2);
  FUN_700b2780(&DAT_701101a3);
  local_b0._0_8_ = s_iBoot_13822_100_791_502_1_7006c280;
  local_b0._8_8_ = s_iBoot_13822_100_791_502_1_7006c280;
  local_a0 = &LAB_7006c300;
  puStack_98 = &LAB_70105fb8;
  FUN_700b2780(s____BUILD_TAG___s_701101da);
  FUN_700b2780(&DAT_701101a3);
  local_b0._0_8_ = &local_90;
  puStack_98 = &LAB_70105fb8;
  local_b0._8_8_ = local_b0._0_8_;
  local_a0 = auStack_6b;
  FUN_700b2780(s____UUID___s_701101ec);
  FUN_700b2780(&DAT_701101a3);
  local_b0._0_8_ = s_RELEASE_7006c240;
  local_b0._8_8_ = s_RELEASE_7006c240;
  local_a0 = &DAT_7006c250;
  puStack_98 = &LAB_70105fb8;
  FUN_700b2780(s____BUILD_STYLE___s_701101f9);
  FUN_700b2780(&DAT_701101a3);
  local_b0 = FUN_70083d24(0);
  puStack_b8 = &LAB_70105fb8;
  local_d0 = puVar5;
  puStack_c8 = puVar5;
  local_c0 = puVar6;
  local_a0 = puVar20;
  puStack_98 = puVar22;
  FUN_700b2780(s_____sSERIAL_NUMBER___s_7011020d);
  FUN_700b2780(&DAT_701101a3);
  FUN_700b2780(s__________________________________70110225);
  FUN_700e72c0();
  FUN_700e70c8(0x20022);
  local_90 = (undefined8 *)((ulong)local_90 & 0xffffffff00000000);
  local_b0._0_8_ = local_b0._0_8_ & 0xffffffff00000000;
  FUN_700c1d50(0x3c504d53,0);
  FUN_70085d68();
  FUN_700c1d50(0x3e504d53,0);
  FUN_700dcc80();
  lVar16 = FUN_700ad6e0(s_nvram_migrate_7011024f,s_nvram_migrate_7011024f,&DAT_7011025d,
                        &LAB_70105fb8);
  if ((lVar16 == 0) || (iVar10 = FUN_700b4550(), iVar10 != 0)) {
    uVar24 = 3;
  }
  else {
    uVar24 = 1;
  }
  FUN_700bc304(uVar24);
  FUN_700c7378(0x2007c00);
  uVar15 = FUN_70083c20();
  iVar10 = 0x20022;
  unaff_w24 = 0x20022;
  if (((uVar15 & 1) == 0) && (iVar13 = thunk_FUN_7008bdc0(), iVar13 != 0)) {
    FUN_7006c930();
  }
  uVar24 = 0x3974bfd3d441da3;
  FUN_700c0228();
  FUN_700819b0();
  iVar11 = FUN_700a959c(&local_90,&local_90,(long)&local_90 + 4,&LAB_70105f78,local_b0,local_b0,
                        local_b0 + 4,&LAB_70105f78);
  iVar13 = 0x20022;
  if (iVar11 == 0) {
    FUN_70070434();
    iVar13 = FUN_700dccc8();
    if ((iVar13 == 0) || ((uint)local_b0._0_4_ < 5)) {
LAB_7006fa18:
      FUN_700bff6c(0);
      iVar13 = unaff_w24;
      goto LAB_7006fa20;
    }
  }
  else {
LAB_7006fa20:
    iVar10 = iVar13;
    uVar15 = FUN_700dccfc();
    if ((uVar15 & 1) != 0) goto LAB_7006fb3c;
    uVar12 = FUN_700ad890(s_auto_boot_once_7011025f,s_auto_boot_once_7011025f,
                          s_upgrade_retry_7011026e,&LAB_70105fb8,1);
    iVar13 = FUN_700ae264(s_auto_boot_once_7011025f,s_auto_boot_once_7011025f,
                          s_upgrade_retry_7011026e,&LAB_70105fb8);
    if (iVar13 != 0) {
      FUN_700e7220(iVar10 + 5,uVar12 & 1);
      FUN_700ae318();
    }
    if ((uVar12 & 1) != 0) {
      FUN_700a94e0(0x12,1);
      uVar15 = FUN_70083c20();
      if ((uVar15 & 1) == 0) {
        FUN_700c1d50(0x3c577552,0);
        uVar14 = thunk_FUN_7008bdc0();
        while ((_DAT_70120f68 != 0 && (iVar13 = FUN_7008b940(), iVar13 != 0))) {
          iVar13 = FUN_700e7db8(_DAT_70120f68,uVar14);
          if (iVar13 != 0) goto LAB_7006fab0;
          FUN_700dc88c(10000);
        }
        FUN_700c1d50(0x3e577552,0);
        ppuVar19 = &PTR_s_fsboot_7011c930;
        pcVar23 = FUN_7006c994;
        ppuVar21 = (undefined **)&DAT_7011caf0;
      }
      else {
        ppuVar19 = &PTR_s_upgrade_7011c850;
        ppuVar21 = &PTR_s_fsboot_7011c930;
        pcVar23 = (code *)0x0;
      }
      FUN_70070084(ppuVar19,ppuVar19,ppuVar21,pcVar23);
      goto LAB_7006fb3c;
    }
  }
LAB_7006fab0:
  FUN_70070434();
LAB_7006fb3c:
  FUN_700e7220(iVar10 + 4,0);
  FUN_700a94e0(0,1);
  bVar9 = FUN_700ad890(s_delay_recovery_image_701100db,s_delay_recovery_image_701100db,
                       s_poweroff_701100f0,&LAB_70105fb8,0);
  DAT_70120f59 = bVar9 & 1;
  if ((bVar9 & 1) == 0) {
    FUN_7006fd1c();
  }
  else {
    _DAT_701288f0 = FUN_700e7d90();
    FUN_700ae264(s_delay_recovery_image_701100db,s_delay_recovery_image_701100db,s_poweroff_701100f0
                 ,&LAB_70105fb8);
    FUN_700ae318();
  }
  FUN_70086a0c();
  uVar15 = (ulong)in_stack_fffffffffffffeb8 & 0xffffffffffffff00;
  FUN_7007044c(s_poweroff_701100f0,extraout_x1,s_Entering_recovery_mode__starting_701100f9);
  FUN_700dc760();
  FUN_700b2780(s_Entering_recovery_mode__starting_701100f9);
  uVar15 = uVar15 & 0xffffffffffffff00;
  FUN_7007044c(s_command_7011012a,extraout_x1_00,s_idle_off_70110132);
  FUN_700dc760();
  uVar17 = FUN_700e7d90();
  local_80 = (undefined8 *)0x0;
  uStack_78 = 0;
  local_90 = (undefined8 *)0x0;
  uStack_88 = 0;
  FUN_700e84c0(&local_90);
  if (local_80 <= local_90) {
                    /* WARNING: Subroutine does not return */
    FUN_700f03f0();
  }
  *local_90 = uVar17;
  uVar18 = FUN_700ad890(s_idle_off_70110132,s_idle_off_70110132,s_idleoff_7011013b,&LAB_70105fb8,0);
  if ((uVar18 & 1) != 0) {
    FUN_700dc69c(s_idleoff_7011013b,s_idleoff_7011013b,s_Remote_70110143,&LAB_70105fb8,FUN_7006ffe8,
                 &PTR_LOOP_70106b50,0,0,0,0,0x400,uVar15 & 0xffffffffffffff00);
    FUN_700dc760();
  }
  FUN_700c1d50(0x3e4d5243,0);
  FUN_700e8540(0,0,0,0);
                    /* WARNING: Subroutine does not return */
  FUN_70089c9c(uVar24,0x5a2);
}



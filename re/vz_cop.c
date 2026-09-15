// ===== 0x10012d99c -> FUN_10012d99c @ 10012d99c

/* WARNING: Function: _objc_retain replaced with injection: _objc_retain_fixup */
/* WARNING: Function: _objc_release replaced with injection: _objc_release_fixup */
/* WARNING: Removing unreachable block (ram,0x00010012dac0) */
/* WARNING: Heritage AFTER dead removal. Example location: x0 : 0x00010012da58 */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */
/* WARNING: Restarted to delay deadcode elimination for space: register */

undefined8 FUN_10012d99c(long param_1,long param_2)

{
  undefined4 uVar1;
  undefined4 uVar2;
  uint uVar3;
  ulong uVar4;
  char *pcVar5;
  long *plVar6;
  undefined8 *puVar7;
  long lVar8;
  ulong uVar9;
  undefined8 uVar10;
  undefined8 uVar11;
  undefined8 uVar12;
  undefined8 *puVar13;
  undefined8 *puVar14;
  void *local_130;
  undefined8 uStack_128;
  long local_120;
  long lStack_118;
  ulong local_110;
  long lStack_108;
  long local_100;
  undefined4 local_f8;
  long local_e8;
  undefined8 local_e0;
  undefined7 local_d8;
  undefined4 uStack_d1;
  undefined1 uStack_cd;
  undefined4 uStack_cc;
  undefined8 uStack_c8;
  void *local_c0;
  undefined8 uStack_b8;
  undefined8 uStack_b0;
  long local_a8;
  ulong local_a0;
  long lStack_98;
  long local_90;
  undefined4 local_88;
  char *local_78;
  undefined8 local_70;
  undefined8 uStack_68;
  undefined1 uStack_59;
  undefined7 *local_58;
  
  uStack_b0 = CONCAT17(10,(undefined7)uStack_b0);
  local_c0 = (void *)s_mailbox_id_1003de66e._0_8_;
  uStack_b8 = CONCAT53(uStack_b8._3_5_,0x6469);
  lVar8 = param_2;
  FUN_10007b114(param_2,&local_c0);
  *(undefined4 *)(param_1 + 0x70) = *(undefined4 *)(*(long *)(lVar8 + 0x28) + 8);
  uStack_b0 = CONCAT17(0xc,(undefined7)uStack_b0);
  local_c0 = (void *)s_base_address_1003dd325._0_8_;
  uStack_b8 = CONCAT35(uStack_b8._5_3_,0x73736572);
  lVar8 = param_2;
  FUN_10007b114(param_2,&local_c0);
  uVar10 = *(undefined8 *)(*(long *)(lVar8 + 0x28) + 8);
  uVar11 = *(undefined8 *)(param_1 + 8);
  pcVar5 = operator_new(lVar8,0x1000c0077774924);
  uVar12 = s_Coprocessor_Mailbox_MMIO_1003d5bd0._0_8_;
  uStack_68 = _UNK_1003af508;
  local_70 = _DAT_1003af500;
  *(undefined8 *)(pcVar5 + 8) = s_Coprocessor_Mailbox_MMIO_1003d5bd0._8_8_;
  *(undefined8 *)pcVar5 = uVar12;
  *(undefined8 *)(pcVar5 + 0x10) = s_Coprocessor_Mailbox_MMIO_1003d5bd0._16_8_;
  pcVar5[0x18] = '\0';
  local_c0 = (void *)CONCAT71(local_c0._1_7_,1);
  uStack_b0 = 4;
  uStack_b8 = 4;
  local_78 = pcVar5;
  FUN_1002893fc(uVar11,uVar10,0x1000,param_1 + 0x48,&local_78,&local_c0);
  pcVar5 = operator_new(pcVar5,0x1000c0077774924);
  uVar12 = s_mailbox_backend_reference_1003de654._0_8_;
  local_d8 = SUB87(pcVar5,0);
  uStack_d1._0_1_ = (char)((ulong)pcVar5 >> 0x38);
  uStack_c8 = _UNK_1003af408;
  uStack_d1._1_3_ = (uint3)_DAT_1003af400;
  uStack_cd = (undefined1)((ulong)_DAT_1003af400 >> 0x18);
  uStack_cc = (undefined4)((ulong)_DAT_1003af400 >> 0x20);
  *(ulong *)(pcVar5 + 8) =
       CONCAT71(s_mailbox_backend_reference_1003de654._9_7_,s_mailbox_backend_reference_1003de654[8]
               );
  *(undefined8 *)pcVar5 = uVar12;
  uVar12 = CONCAT17(s_mailbox_backend_reference_1003de654[0x10],
                    s_mailbox_backend_reference_1003de654._9_7_);
  *(undefined8 *)(pcVar5 + 0x11) = s_mailbox_backend_reference_1003de654._17_8_;
  *(undefined8 *)(pcVar5 + 9) = uVar12;
  pcVar5[0x19] = '\0';
  lVar8 = param_2;
  FUN_10008d36c(param_2,&local_d8);
  lVar8 = *(long *)(lVar8 + 0x28);
  uStack_b8 = *(undefined8 *)(lVar8 + 0x10);
  local_c0 = *(void **)(lVar8 + 8);
  uStack_b0 = *(long *)(lVar8 + 0x18);
  local_a8 = *(long *)(lVar8 + 0x20);
  *(undefined8 *)(lVar8 + 8) = 0;
  *(undefined8 *)(lVar8 + 0x10) = 0;
  *(undefined8 *)(lVar8 + 0x18) = 0;
  *(undefined8 *)(lVar8 + 0x20) = 0;
  lStack_98 = *(long *)(lVar8 + 0x30);
  local_a0 = *(ulong *)(lVar8 + 0x28);
  *(undefined8 *)(lVar8 + 0x28) = 0;
  local_90 = *(long *)(lVar8 + 0x38);
  local_88 = *(undefined4 *)(lVar8 + 0x40);
  if (local_90 != 0) {
    uVar9 = *(ulong *)(*(long *)(lVar8 + 0x30) + 8);
    if ((local_a0 & local_a0 - 1) == 0) {
      uVar9 = local_a0 - 1 & uVar9;
    }
    else if (local_a0 <= uVar9) {
      uVar4 = 0;
      if (local_a0 != 0) {
        uVar4 = uVar9 / local_a0;
      }
      uVar9 = uVar9 - uVar4 * local_a0;
    }
    *(long **)(local_a8 + uVar9 * 8) = &lStack_98;
    *(long *)(lVar8 + 0x30) = 0;
    *(undefined8 *)(lVar8 + 0x38) = 0;
  }
  operator_delete(pcVar5);
  if (DAT_100455958 != -1) {
    local_d8 = SUB87(&uStack_59,0);
    uStack_d1._0_1_ = (char)((ulong)&uStack_59 >> 0x38);
    local_58 = &local_d8;
    std::__call_once((ulong *)&DAT_100455958,&local_58,FUN_10012c560);
  }
  local_110 = local_a0;
  lStack_118 = local_a8;
  local_120 = uStack_b0;
  uVar12 = DAT_100455950;
  local_e8 = *(long *)(param_1 + 0x60);
  uStack_128 = uStack_b8;
  local_130 = local_c0;
  local_c0 = (void *)0x0;
  uStack_b8 = 0;
  local_a8 = 0;
  local_a0 = 0;
  uStack_b0 = 0;
  lStack_108 = lStack_98;
  local_100 = local_90;
  local_f8 = local_88;
  if (local_90 != 0) {
    uVar9 = *(ulong *)(lStack_98 + 8);
    if ((local_110 & local_110 - 1) == 0) {
      uVar9 = local_110 - 1 & uVar9;
    }
    else if (local_110 <= uVar9) {
      uVar4 = 0;
      if (local_110 != 0) {
        uVar4 = uVar9 / local_110;
      }
      uVar9 = uVar9 - uVar4 * local_110;
    }
    *(long **)(lStack_118 + uVar9 * 8) = &lStack_108;
    lStack_98 = 0;
    local_90 = 0;
  }
  FUN_10012c1c8(&local_e0,uVar12,param_1 + 0x58,&local_e8,&local_130);
  plVar6 = *(long **)(param_1 + 0x68);
  *(undefined8 *)(param_1 + 0x68) = local_e0;
  if (plVar6 != (long *)0x0) {
    (**(code **)(*plVar6 + 8))();
  }
  FUN_10038465c(&lStack_118);
  if (local_120 < 0) {
    operator_delete(local_130);
  }
  uStack_c8 = CONCAT17(0xb,(undefined7)uStack_c8);
  local_d8 = (undefined7)s_irq_numbers_1003de679._0_8_;
  uStack_d1._0_1_ = SUB81(s_irq_numbers_1003de679._0_8_,7);
  uStack_d1 = CONCAT31(0x737265,(char)uStack_d1);
  uStack_cd = 0;
  FUN_10007b114(param_2,&local_d8);
  uVar1 = *(undefined4 *)(*(long *)(param_2 + 0x28) + 8);
  uVar2 = *(undefined4 *)(*(long *)(param_2 + 0x28) + 0xc);
  uVar12 = *(undefined8 *)(*(long *)(param_1 + 8) + 8);
  puVar7 = operator_new(param_2,0x10a1c40df6760fd);
  *puVar7 = &PTR_FUN_100448950;
  puVar7[1] = uVar12;
  *(undefined4 *)(puVar7 + 2) = uVar1;
  plVar6 = *(long **)(param_1 + 0xe0);
  *(undefined8 **)(param_1 + 0xe0) = puVar7;
  if ((plVar6 == (long *)0x0) || ((**(code **)(*plVar6 + 8))(), *(long *)(param_1 + 0xe0) != 0)) {
    uVar12 = *(undefined8 *)(*(long *)(param_1 + 8) + 8);
    puVar7 = operator_new(plVar6,0x10a1c40df6760fd);
    *puVar7 = &PTR_FUN_100448950;
    puVar7[1] = uVar12;
    *(undefined4 *)(puVar7 + 2) = uVar2;
    plVar6 = *(long **)(param_1 + 0xe8);
    *(undefined8 **)(param_1 + 0xe8) = puVar7;
    if ((plVar6 == (long *)0x0) || ((**(code **)(*plVar6 + 8))(), *(long *)(param_1 + 0xe8) != 0)) {
      lVar8 = *(long *)(param_1 + 8);
      uVar3 = *(uint *)(param_1 + 0x70);
      puVar7 = *(undefined8 **)(lVar8 + 0x1d8);
      if (*(undefined8 **)(lVar8 + 0x1d8) == (undefined8 *)0x0) {
        puVar13 = (undefined8 *)(lVar8 + 0x1d8);
        puVar14 = puVar13;
      }
      else {
        do {
          while (puVar13 = puVar7, uVar3 < *(uint *)(puVar13 + 4)) {
            puVar7 = (undefined8 *)*puVar13;
            puVar14 = puVar13;
            if ((undefined8 *)*puVar13 == (undefined8 *)0x0) goto LAB_10012de4c;
          }
          if (uVar3 <= *(uint *)(puVar13 + 4)) goto LAB_10012dea4;
          puVar7 = (undefined8 *)puVar13[1];
        } while ((undefined8 *)puVar13[1] != (undefined8 *)0x0);
        puVar14 = puVar13 + 1;
      }
LAB_10012de4c:
      puVar7 = operator_new(plVar6,0x1020c002c67df80);
      *(uint *)(puVar7 + 4) = uVar3;
      puVar7[5] = param_1 + 0x50;
      *puVar7 = 0;
      puVar7[1] = 0;
      puVar7[2] = puVar13;
      *puVar14 = puVar7;
      if (**(long **)(lVar8 + 0x1d0) != 0) {
        *(long *)(lVar8 + 0x1d0) = **(long **)(lVar8 + 0x1d0);
      }
      FUN_1000aad7c(*(undefined8 *)(lVar8 + 0x1d8));
      *(long *)(lVar8 + 0x1e0) = *(long *)(lVar8 + 0x1e0) + 1;
LAB_10012dea4:
      local_d8 = 0x10012df64;
      uStack_d1._1_3_ = (uint3)param_1;
      uStack_d1 = (uint)uStack_d1._1_3_ << 8;
      uStack_cd = (undefined1)((ulong)param_1 >> 0x18);
      uStack_cc = (undefined4)((ulong)param_1 >> 0x20);
      _dispatch_sync_f(*(dispatch_queue_t *)(param_1 + 0x60),(void *)((long)&uStack_d1 + 1),
                       FUN_10012df64);
      uVar12 = 1;
      goto LAB_10012ded4;
    }
  }
  uVar12 = 0;
LAB_10012ded4:
  FUN_10038465c(&local_a8);
  if (uStack_b0 < 0) {
    operator_delete(local_c0);
  }
  return uVar12;
}



// ===== 0x00125254 -> FUN_00125254 @ 00125254

undefined1  [16] FUN_00125254(long param_1)

{
  ulong uVar1;
  undefined8 uVar2;
  undefined8 in_x4;
  undefined8 in_x5;
  undefined8 in_x6;
  undefined8 in_x7;
  undefined8 unaff_x19;
  undefined4 *unaff_x20;
  undefined4 *unaff_x21;
  undefined4 *unaff_x22;
  undefined1 auVar3 [16];
  ulong in_stack_00000000;
  uint in_stack_00000008;
  
  if (param_1 != 0) {
    FUN_00126080();
    FUN_001261a0();
    uVar1 = FUN_00110ac4();
    if ((in_stack_00000008 != 0 && uVar1 < 0x10) && (in_stack_00000008 & in_stack_00000008 - 1) == 0
       ) {
      FUN_0012600c();
      FUN_001113a0();
      if (unaff_x21 <= unaff_x22 && unaff_x22 < unaff_x20) {
        FUN_001261cc();
        FUN_001109fc(unaff_x22 + 0x14,unaff_x22 + 0x14,unaff_x22 + 0x18,0x70029d98,in_x4,in_x5,in_x6
                     ,in_x7);
        *unaff_x22 = 0;
        *(undefined1 *)(unaff_x22 + 1) = 0;
        unaff_x22[2] = in_stack_00000008;
        uVar1 = FUN_0010eed4(in_stack_00000008);
        unaff_x22[6] = (int)uVar1;
        uVar1 = in_stack_00000000 >> (uVar1 & 0x3f);
        *(ulong *)(unaff_x22 + 4) = uVar1;
        *(ulong *)(unaff_x22 + 8) = in_stack_00000000;
        *(undefined8 *)(unaff_x22 + 10) = 1;
        if (uVar1 == 0xffffffffffffffff) goto LAB_00125448;
        uVar2 = FUN_0012c8c0(0);
        auVar3._0_8_ = thunk_FUN_0012c6d8(uVar2,1,0x1000,0x1000);
        FUN_001113a0(auVar3._0_8_,auVar3._0_8_,auVar3._0_8_ + 0xf8,&PTR_LOOP_00140368,0,0xf8);
        FUN_00126038(auVar3._0_8_,auVar3._0_8_,auVar3._0_8_ + 0x60,0x70029db0);
        FUN_00111154();
        *(code **)(auVar3._0_8_ + 0x60) = FUN_00125454;
        *(undefined ***)(auVar3._0_8_ + 0x68) = &PTR_LOOP_00140318;
        *(code **)(auVar3._0_8_ + 0x70) = FUN_00125a10;
        *(undefined ***)(auVar3._0_8_ + 0x78) = &PTR_LOOP_0013e490;
        *(code **)(auVar3._0_8_ + 0x80) = FUN_00125a3c;
        *(undefined ***)(auVar3._0_8_ + 0x88) = &PTR_LOOP_00140318;
        *(code **)(auVar3._0_8_ + 0x90) = FUN_00125ed8;
        *(undefined ***)(auVar3._0_8_ + 0x98) = &PTR_LOOP_0013e490;
        *(code **)(auVar3._0_8_ + 0xa0) = FUN_00125f04;
        *(undefined ***)(auVar3._0_8_ + 0xa8) = &PTR_LOOP_00140340;
        *(code **)(auVar3._0_8_ + 0xb0) = FUN_00125f30;
        *(undefined ***)(auVar3._0_8_ + 0xb8) = &PTR_LOOP_0013e490;
        *(undefined4 **)(auVar3._0_8_ + 0xd0) = unaff_x22;
        *(undefined4 **)(auVar3._0_8_ + 0xd8) = unaff_x21;
        *(undefined4 **)(auVar3._0_8_ + 0xe0) = unaff_x20;
        *(undefined8 *)(auVar3._0_8_ + 0xe8) = unaff_x19;
        auVar3._8_8_ = auVar3._0_8_;
        return auVar3;
      }
                    /* WARNING: Subroutine does not return */
      FUN_0012ea7c();
    }
  }
  uVar2 = 0x95;
  do {
    FUN_00126020(uVar2);
    FUN_001260a0();
LAB_00125448:
    uVar2 = 0xa1;
  } while( true );
}



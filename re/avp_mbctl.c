// ===== 0x10d814 -> FUN_0010d814 @ 0010d814

void FUN_0010d814(void)

{
  code *pcVar1;
  ulong unaff_x30;
  
  if (((unaff_x30 ^ unaff_x30 << 1) >> 0x3e & 1) != 0) {
                    /* WARNING: Does not return */
    pcVar1 = (code *)SoftwareBreakpoint(0xc471,0x10d840);
    (*pcVar1)();
  }
  FUN_0010d578();
  return;
}


// ===== 0x10d844 -> FUN_0010d844 @ 0010d844

void FUN_0010d844(undefined8 param_1)

{
  code *pcVar1;
  ulong unaff_x30;
  undefined8 uStack0000000000000000;
  undefined8 uStack0000000000000008;
  
  uStack0000000000000000 = 0xbab0172d798c3be;
  uStack0000000000000008 = param_1;
  if (((unaff_x30 ^ unaff_x30 << 1) >> 0x3e & 1) != 0) {
                    /* WARNING: Does not return */
    pcVar1 = (code *)SoftwareBreakpoint(0xc471,0x10d86c);
    (*pcVar1)();
  }
  FUN_0010f150(s__llx__d_0014678f);
  return;
}



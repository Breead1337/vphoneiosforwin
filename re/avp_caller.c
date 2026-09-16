// ===== 0x0012bf00 -> FUN_0012becc @ 0012becc

void FUN_0012becc(undefined8 *param_1,ulong *param_2,ulong *param_3,int param_4)

{
  ulong *puVar1;
  ulong *puVar2;
  
  puVar1 = param_2;
  if (*param_2 != 0) {
    puVar1 = (ulong *)(*param_2 & 0xfffffffffffffff8);
  }
  puVar2 = param_3;
  if (*param_3 != 0) {
    puVar2 = (ulong *)(*param_3 & 0xfffffffffffffff8);
  }
  if (puVar1 != puVar2) {
    if (param_4 != 0) {
      FUN_0012cc30();
      return;
    }
    *param_1 = 0;
    param_1[1] = &DAT_0014684a;
    param_1[2] = param_2;
    param_1[3] = param_3;
    return;
  }
  *param_1 = 1;
  param_1[1] = 0;
  param_1[2] = 0;
  param_1[3] = 0;
  return;
}



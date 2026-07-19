void* fn_27_1B014C(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 28) + i;
    if (idx >= 4) idx -= 4;
    return (char*)p + idx * 184 + 12;
}

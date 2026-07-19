void* fn_27_D8FF8(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 28) + i;
    if (idx >= 7) idx -= 7;
    return (char*)p + idx * 16 + 12;
}

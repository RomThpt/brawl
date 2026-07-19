void* fn_27_D9548(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 26) + i;
    if (idx >= 23) idx -= 23;
    return (char*)p + idx * 48 + 12;
}

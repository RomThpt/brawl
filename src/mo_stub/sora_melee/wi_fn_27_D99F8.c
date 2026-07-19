void* fn_27_D99F8(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 24) + i;
    if (idx >= 70) idx -= 70;
    return (char*)p + idx * 8 + 12;
}

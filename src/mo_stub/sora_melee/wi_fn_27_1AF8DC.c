void* fn_27_1AF8DC(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 22) + i;
    if (idx >= 287) idx -= 287;
    return (char*)p + idx * 4 + 12;
}

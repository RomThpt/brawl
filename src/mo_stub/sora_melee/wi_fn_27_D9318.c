void* fn_27_D9318(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 25) + i;
    if (idx >= 38) idx -= 38;
    return (char*)p + idx * 48 + 12;
}

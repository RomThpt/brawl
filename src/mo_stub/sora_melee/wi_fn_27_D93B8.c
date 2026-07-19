void* fn_27_D93B8(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 25) + i;
    if (idx >= 33) idx -= 33;
    return (char*)p + idx * 48 + 12;
}

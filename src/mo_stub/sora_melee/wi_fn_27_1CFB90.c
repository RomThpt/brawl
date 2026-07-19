void* fn_27_1CFB90(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 26) + i;
    if (idx >= 18) idx -= 18;
    return (char*)p + idx * 12 + 12;
}

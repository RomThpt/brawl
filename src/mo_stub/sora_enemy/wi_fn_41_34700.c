void* fn_41_34700(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 28) + i;
    if (idx >= 7) idx -= 7;
    return (char*)p + idx * 16 + 12;
}

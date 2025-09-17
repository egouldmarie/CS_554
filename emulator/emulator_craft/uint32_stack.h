/* uint32_stack.h */

#ifndef UINT32_STACK_H
#define UINT32_STACK_H

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

// Struct definitions
struct StackNode {
    uint32_t data;
    struct StackNode* next;
};

// Function prototypes

int isEmpty(struct StackNode* top);
struct StackNode* newNode(uint32_t data);
uint32_t peek(struct StackNode* top);
uint32_t pop(struct StackNode** top_ref);
void push(struct StackNode** top_ref, uint32_t data);

#endif // UINT32_STACK_H
/**
 * Implementation of a uint32_t stack using a linked list.
 * Based on discussion and code at
 * https://www.geeksforgeeks.org/c/stack-using-linked-list-in-c/
 * and https://www.digitalocean.com/community/tutorials/stack-in-c 
 * (mostly borrowing code from the latter).
*/

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include "uint32_stack.h"

// struct StackNode {
//     uint32_t data;
//     struct StackNode* next;
// };

struct StackNode* newNode(uint32_t data) {
    struct StackNode* stackNode = (struct StackNode*)malloc(sizeof(struct StackNode));
    if (!stackNode) {
        printf("WARNING: Heap Overflow in UINT32 Stack.\n");
        return NULL;
    }
    stackNode->data = data;
    stackNode->next = NULL;
    return stackNode;
}

int isEmpty(struct StackNode* top) {
    return !top;
}

void push(struct StackNode** top_ref, uint32_t data) {
    struct StackNode* stackNode = newNode(data);
    if (!stackNode) return;
    stackNode->next = *top_ref;
    *top_ref = stackNode;
    // printf("%d pushed to stack\n", data);
}

uint32_t pop(struct StackNode** top_ref) {
    if (isEmpty(*top_ref)) {
        printf("WARNING: Stack Underflow in UINT32 Stack.\n");
        return UINT32_MAX;
    }
    struct StackNode* temp = *top_ref;
    uint32_t popped = temp->data;
    *top_ref = (*top_ref)->next;

    free(temp);

    // printf("%d popped off stack\n", popped);

    return popped;
}

uint32_t peek(struct StackNode* top) {
    if (isEmpty(top)) {
        // printf("Stack is empty\n");
        return UINT32_MAX;
    }
    return top->data;
}

// === for testing === //

// int main() {
//     // testing

//     struct StackNode* top = NULL;

//     push(&top, 10);
//     push(&top, 20);
//     push(&top, 30);

//     printf("\nTop element is %u\n", peek(top));

//     printf("%u popped from stack\n", pop(&top));

//     printf("\nTop element is %u\n", peek(top));

//     printf("\nPopping all elements:\n");
//     while (!isEmpty(top)) {
//         printf("%u popped from stack\n", pop(&top));
//     }

//     printf("\nTry popping once again:\n");
//     pop(&top);

//     printf("\n\n");


//     return 0;
// }
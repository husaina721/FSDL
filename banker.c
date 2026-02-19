#include <stdio.h>
#include <stdbool.h>

#define P 10   // Max processes
#define R 10   // Max resources

int alloc[P][R], max[P][R], need[P][R], avail[R];
int n, m;  // n = processes, m = resources

// Function to calculate Need matrix
void calculateNeed() {
    for (int i = 0; i < n; i++)
        for (int j = 0; j < m; j++)
            need[i][j] = max[i][j] - alloc[i][j];
}

// Function to print tables
void printTable() {
    printf("\nProcess\tAllocation\tMax\t\tNeed\n");
    for (int i = 0; i < n; i++) {
        printf("P%d\t", i);
        for (int j = 0; j < m; j++)
            printf("%d ", alloc[i][j]);
        printf("\t\t");
        for (int j = 0; j < m; j++)
            printf("%d ", max[i][j]);
        printf("\t\t");
        for (int j = 0; j < m; j++)
            printf("%d ", need[i][j]);
        printf("\n");
    }

    printf("\nAvailable: ");
    for (int i = 0; i < m; i++)
        printf("%d ", avail[i]);
    printf("\n");
}

// Safety Algorithm
bool isSafe() {
    bool finish[P] = {0};
    int work[R];
    for (int i = 0; i < m; i++) work[i] = avail[i];

    int safeSeq[P], count = 0;

    while (count < n) {
        bool found = false;
        for (int p = 0; p < n; p++) {
            if (!finish[p]) {
                int j;
                for (j = 0; j < m; j++)
                    if (need[p][j] > work[j])
                        break;

                if (j == m) {
                    for (int k = 0; k < m; k++)
                        work[k] += alloc[p][k];
                    safeSeq[count++] = p;
                    finish[p] = 1;
                    found = true;
                }
            }
        }
        if (!found) {
            printf("\nSystem is NOT in a Safe State!\n");
            return false;
        }
    }

    printf("\nSystem is in a Safe State.\nSafe Sequence: ");
    for (int i = 0; i < n; i++)
        printf("P%d ", safeSeq[i]);
    printf("\n");

    return true;
}

// Request Algorithm
bool requestResources(int process, int request[]) {
    for (int i = 0; i < m; i++) {
        if (request[i] > need[process][i]) {
            printf("Error: P%d has exceeded its maximum claim.\n", process);
            return false;
        }
    }
    for (int i = 0; i < m; i++) {
        if (request[i] > avail[i]) {
            printf("Process P%d must wait since resources are not available.\n", process);
            return false;
        }
    }

    for (int i = 0; i < m; i++) {
        avail[i] -= request[i];
        alloc[process][i] += request[i];
        need[process][i] -= request[i];
    }

    if (isSafe()) {
        printf("Request can be granted to P%d.\n", process);
        return true;
    } else {
        for (int i = 0; i < m; i++) {
            avail[i] += request[i];
            alloc[process][i] -= request[i];
            need[process][i] += request[i];
        }
        printf("Request cannot be granted to P%d (Unsafe State).\n", process);
        return false;
    }
}

int main() {
    printf("Enter number of processes: ");
    scanf("%d", &n);

    printf("Enter number of resources: ");
    scanf("%d", &m);

    printf("Enter Allocation Matrix (%d x %d):\n", n, m);
    for (int i = 0; i < n; i++)
        for (int j = 0; j < m; j++)
            scanf("%d", &alloc[i][j]);

    printf("Enter Maximum Matrix (%d x %d):\n", n, m);
    for (int i = 0; i < n; i++)
        for (int j = 0; j < m; j++)
            scanf("%d", &max[i][j]);

    printf("Enter Available Resources (%d):\n", m);
    for (int i = 0; i < m; i++)
        scanf("%d", &avail[i]);

    calculateNeed();

    // Print matrices
    printTable();

    // Initial safety check
    isSafe();

    // Resource Request Example
    int process;
    printf("\nEnter process number for request (0-%d): ", n-1);
    scanf("%d", &process);

    int request[R];
    printf("Enter request for P%d (%d values): ", process, m);
    for (int i = 0; i < m; i++)
        scanf("%d", &request[i]);

    requestResources(process, request);

    return 0;
}

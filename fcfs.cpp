#include <stdio.h>

struct Process {
    int pid;
    int at, bt, ct, tat, wt;
};

int main() {
    int n;
    printf("Enter number of processes: ");
    scanf("%d",&n);

    struct Process p[n];

    // Input process details
    for (int i = 0; i < n; i++) {
        p[i].pid = i + 1;
        printf("Enter Arrival Time and Burst Time for P%d: ", p[i].pid);
        scanf("%d %d", &p[i].at, &p[i].bt);
    }

    // Sort by Arrival Time
    for (int i = 0; i < n - 1; i++) {
        for (int j = i + 1; j < n; j++) {
            if (p[i].at > p[j].at) {
                struct Process temp = p[i];
                p[i] = p[j];
                p[j] = temp;
            }
        }
    }

    int current_time = 0;
    float total_tat = 0, total_wt = 0;

    // Calculate CT, TAT, WT
    for (int i = 0; i < n; i++) {
        if (current_time < p[i].at)
            current_time = p[i].at;

        p[i].ct = current_time + p[i].bt;
        p[i].tat = p[i].ct - p[i].at;
        p[i].wt = p[i].tat - p[i].bt;

        current_time = p[i].ct;

        total_tat += p[i].tat;
        total_wt += p[i].wt;
    }

    // Output table
    printf("\nPID\tAT\tBT\tCT\tTAT\tWT\n");
    for (int i = 0; i < n; i++) {
        printf("P%d\t%d\t%d\t%d\t%d\t%d\n", p[i].pid, p[i].at, p[i].bt, p[i].ct, p[i].tat, p[i].wt);
    }

    // Gantt chart
    printf("\nGantt Chart:\n|");
    for (int i = 0; i < n; i++) {
        printf("  P%d  |", p[i].pid);
    }

    printf("\n0");
    for (int i = 0; i < n; i++) {
        printf("     %d", p[i].ct);
    }

    // Averages
    printf("\n\nAverage TAT: %.2f", total_tat / n);
    printf("\nAverage WT : %.2f\n", total_wt / n);

    return 0;
}
package sortAlgorithms;

import java.util.Random;

public class SortingArraysSpaceDep {
    // merge sort = recursively divide array in 2, sort, re-combine
    // run-time complexity = O(n Log n)
    // space complexity    = O(n)

    public static void main(String[] args) {
        Random rand = new Random();

        int[] array = new int[100000];
        for (int i = 0; i < 100000; i++){
            array[i] = rand.nextInt(10000);
        }

        long startTime, endTime, elapsedTime;

        startTime = System.nanoTime();

        mergeSort(array);

        endTime = System.nanoTime();

        elapsedTime = endTime - startTime;
        System.out.println("Done is:\t" + elapsedTime/1000000 + "ms");
    }

    private static void mergeSort(int[] array) {
        int length = array.length;
        if (length <= 1) return; //base case

        int middle = length / 2;
        int[] leftArray = new int[middle];
        int[] rightArray = new int[length - middle];

        int i = 0; //left array
        int j = 0; //right array

        for(; i < length; i++) {
            if(i < middle) {
                leftArray[i] = array[i];
            }
            else {
                rightArray[j] = array[i];
                j++;
            }
        }
        mergeSort(leftArray);
        mergeSort(rightArray);
        merge(leftArray, rightArray, array);
    }

    private static void merge(int[] leftArray, int[] rightArray, int[] array) {
        int leftSize = array.length / 2;
        int rightSize = array.length - leftSize;
        int i = 0, l = 0, r = 0; //indices

        //check the conditions for merging
        while(l < leftSize && r < rightSize) {
            if(leftArray[l] < rightArray[r]) {
                array[i] = leftArray[l];
                i++;
                l++;
            }
            else {
                array[i] = rightArray[r];
                i++;
                r++;
            }
        }
        while(l < leftSize) {
            array[i] = leftArray[l];
            i++;
            l++;
        }
        while(r < rightSize) {
            array[i] = rightArray[r];
            i++;
            r++;
        }
    }
}

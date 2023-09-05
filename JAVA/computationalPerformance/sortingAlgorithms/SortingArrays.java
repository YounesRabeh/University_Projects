package sortAlgorithms;

import java.util.Arrays;
import java.util.Random;

public class SortingArrays {
    // bubble sort = pairs of adjacent elements are compared, and the elements
    //		            swapped if they are not in order.

    //				 Quadratic time O(n^2)
    //				 small data set = okay-ish
    //				 large data set = BAD (plz don't)

    // selection sort = search through an array and keep track of the minimum value during
    //			         each iteration. At the end of each iteration, we swap values.

    //				 Quadratic time O(n^2)
    //				 small data set = okay
    //				 large data set = BAD

    // Insertion sort = after comparing elements to the left,
    //				shift elements to the right to make room to insert a value

    //				Quadratic time O(n^2)
    //				small data set = decent
    //				large data set = BAD

    //				Fewer steps than Bubble sort
    //				Best case is O(n) compared to Selection sort O(n^2)



    public static void main(String[] args) {
        Random rand = new Random();

        int[] array = new int[100000];
        for (int i = 0; i < 100000; i++){
            array[i] = rand.nextInt(10000);
        }

        long startTime, endTime, elapsedTime;

        startTime = System.nanoTime();

        //bubbleSort(array);
        //selectionSort(array);
        insertionSort(array);

        endTime = System.nanoTime();

        elapsedTime = endTime - startTime;

        //System.out.println(Arrays.toString(array));
        System.out.println("Done is:\t" + elapsedTime/1000000 + "ms");

    }

     static void bubbleSort(int[] array) {
        for(int i = 0; i < array.length - 1; i++) {
            for(int j = 0; j < array.length - i - 1; j++) {
                if(array[j] > array[j+1]) {
                    int temp = array[j];
                    array[j] = array[j+1];
                    array[j+1] = temp;
                }
            }
        }
    }

    static void selectionSort(int[] array) {
        for(int i = 0; i < array.length - 1; i++) {
            int min = i;
            for(int j = i + 1; j < array.length; j++) {
                if(array[min] > array[j]) {
                    min = j;
                }
            }

            int temp = array[i];
            array[i] = array[min];
            array[min] = temp;
        }

    }

     static void insertionSort(int[] array) {

        for(int i = 1; i < array.length; i++) {
            int temp = array[i];
            int j = i - 1;

            while(j >= 0 && array[j] > temp) {
                array[j + 1] = array[j];
                j--;
            }
            array[j + 1] = temp;
        }
    }
}

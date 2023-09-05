package dataTypes;

import java.util.ArrayList;
import java.util.LinkedList;

public class LinkedListsVsArrayList {

    public static void main(String[] args) {

        LinkedList<Integer> linkedList = new LinkedList<Integer>();
        ArrayList<Integer> arrayList = new ArrayList<Integer>();

        long startTime;
        long endTime;
        long elapsedTime;

        for(int i = 0; i < 1000000; i++){
            linkedList.add(i);
            arrayList.add(i);
        }

        // ****************LinkedList****************
        startTime = System.nanoTime();

        //linkedList.get(0); //BEST
        linkedList.get(500000); //WORST bz: a doubly linked list
        //linkedList.get(999999); //BEST bz: a doubly linked list if not this is the worst case
        //linkedList.remove(0);
        //linkedList.remove(500000);
        //linkedList.remove(999999);

        endTime = System.nanoTime();

        elapsedTime = endTime - startTime;

        System.out.println("LinkedList :\t" + elapsedTime +" ns");

        // ****************ArrayList****************

        startTime = System.nanoTime();

        //arrayList.get(0);      //SAME
        arrayList.get(500000); //SAME
        //arrayList.get(999999); //SAME
        //arrayList.remove(0);   //WORST
        //arrayList.remove(500000); //MED
        //arrayList.remove(999999);  //BEST

        endTime = System.nanoTime();

        elapsedTime = endTime - startTime;

        System.out.println("ArrayList  :\t" + elapsedTime +" ns");

    }
}
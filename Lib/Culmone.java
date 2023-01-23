package Lib;

import java.util.Random;

/** The best Library in Camerino*/
public final class Culmone {
    private Culmone(){}

    /**Generate a <b>random number</b>
     * @param origin the low bound (min value)
     * @param bound the high bound (max value)
     * @return a random int between ORIGIN and BOUND
     * */
    public static int random(int origin, int bound){
        Random rand = new Random();
        return rand.nextInt(origin,  bound + 1);
    }

    /**Fuse <b>2 Arrays</b> together*/

    public static int[] arrayFusion(int[] a, int[] b) {
        int result = 0;
        int _a = a.length; int _b = b.length;
        int l = _a + _b;
        int[] c = new int[l];
        System.arraycopy(a, 0, c, 0, l - _b);
        return c;
    }

    /**Calculate the factorial <b>n!</b>
     * @param n the number (int)
     * @return the factorial of n*/
    public static int factorial(int n){
        if (n<0){
            throw new RuntimeException(RED_BOLD + "[!!]-NEGATIVE PARAMETER" + RESET);
        } else {
            return n == 0 ? 1 : n * factorial(n-1);
        }
    }

    /**Calculate the <b>Binomial Coefficient</b> (n k)
     * @return the Binomial Coefficient*/
    public static int binomialCoefficient(int n, int k){
        if (n < k){
            throw new RuntimeException(RED_BOLD + "[!!]-n IS SMALLER THAN k" + RESET);
        } else {
            return factorial(n) / (factorial(k) * factorial(n - k));
        }
    }

    /**Calculate the <b>fibonacci series</b> of a given number
     * @param k the parameter of the fibonacci series*/
    public static long fibonacci(long k){
        long n = 1; long m = 0;
        while (k > 0){
            n = m + n; m = n - m;
            k--;
        }
        return m;
    }

    public static final String RESET = "\033[0m";  // Text Reset
    public static final String RED_BOLD = "\033[1;31m";    // RED
    public static final String GREEN_BOLD = "\033[1;32m";  // GREEN
    public static final String YELLOW_BOLD = "\033[1;33m"; // YELLOW
    public static final String BLUE_BOLD = "\033[1;34m";   // BLUE
    public static final String PURPLE_BOLD = "\033[1;35m"; // PURPLE
    public static final String CYAN_BOLD = "\033[1;36m";   // CYAN
    public static final String YELLOW_BOLD_BRIGHT = "\033[1;93m";// YELLOW
    public static final String PURPLE_BOLD_BRIGHT = "\033[1;95m";// PURPLE
    public static final String WHITE_BOLD_BRIGHT = "\033[1;97m"; // WHITE

    private static final String[] colors = {RED_BOLD, YELLOW_BOLD, GREEN_BOLD, CYAN_BOLD, PURPLE_BOLD, WHITE_BOLD_BRIGHT,
            BLUE_BOLD, YELLOW_BOLD_BRIGHT, PURPLE_BOLD_BRIGHT};
    /**Print a <b>gay</b> text
     * @param text the String that you want to print
     * */
    public static void printGayText(String text){
        int x = text.length();
        int colorIndex = 0;
        char[] characters = text.toCharArray();
        System.out.print("\n");
        for (int i = 0; i < x; i++){
            if (colorIndex >= colors.length){colorIndex = 0;}
            System.out.print(colors[colorIndex] + characters[i]);
            colorIndex++;
        }
        System.out.print("\n");
    }

    /**Used to calculate <b>2D Matrices</b>
     * <li>The matrices are defined:</li>
     * <p>int[][] _name_ = {row 1{column1, column2, ...}, row2{column1, column2, ...}, ...}</p>
     * @param A the FIRST matrix
     * @param B the Second matrix
     * @return The matrix AB [A x B]*/
    public static int[][] matrixMultiplication(int[][] A, int[][] B){
        int lines = A.length;
        int columns = B[0].length;
        if(lines != columns ){
            throw new RuntimeException(ConsoleColors.RED_BOLD + "[!!]-MATRIX SIZE ERROR" +
                    ConsoleColors.RESET);
        }
        int[][] c = new int[lines][columns];
        for (int i = 0; i < lines; i++){
            for (int j = 0; j < lines; j++){
                c[i][j] = 0;
                for (int k = 0; k < lines; k++){
                    c[i][j] += A[i][k] * B[k][j];
                }
            }
        }
        return c;
    }

}

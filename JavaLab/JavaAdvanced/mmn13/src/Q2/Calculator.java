package Q2;

import java.util.*;
import static java.lang.Math.*;
import java.lang.*;


/**
 * calculate an Arithmetic expression with out taking the order of operations in accaunt.
 */
public class Calculator {
    public boolean status; // status if the solve of the expression success.
    public double result; // the result of the expression
    private ArrayList<Object> ls; //aray list that will contain the numbers + action in the way they appear in the beginning text.
    private String evaluation; // the evaluation in a string (this is what we are starting with)

    /**
     * empty constractor
     */
    public Calculator(){
        ls = new ArrayList<Object>();
        evaluation ="";
    }

    /**
     * first separate the evaluation to array of numbers and action and then solve it.
     * Assumption: The text has been properly proofed and includes a sequence of "number + action + number"
     * @param calc the evaluation  to solve as string
     * @throws CalculatorError if there is an error so it throw this with the explain in the text
     */
    public void runQuery(String calc) throws CalculatorError{
        ls = new ArrayList<Object>();
        evaluation = calc;
        status = false;
        toArray();
        System.out.printf("%s%n",ls.toString());
        Calculate();

    }

    /**
     * separate the evaluation to array of numbers and action.
     * Assumption: The text has been properly proofed and includes a sequence of "number + action + number"
     * @throws RuntimeException
     */
    public void toArray() throws RuntimeException{
        int start = 0,end;
        char c;
        int i=0,sign=1;
        while (i<evaluation.length()){
            c = evaluation.charAt(i);
            if (c == '('){
                sign = sign*-1;
                i += 5;
                start = i;
                continue;
            }
            if ((c>='0' && c<='9') || c=='.')
            {
                i+=1;
                continue;
            }
            if (c == '+' || c == '-' || c == '*' || c== '/'){
                end = i;
                String numberSt = evaluation.substring(start,end);
                double number = Double.parseDouble(numberSt);
                number = number * sign;
                ls.add(number);
                ls.add(c);
                i+=1;
                sign=1;
                start = i;
                continue;
            }
            throw new RuntimeException();
        }
        end = i;
        String numberSt = evaluation.substring(start,end);
        double number = Double.parseDouble(numberSt);
        number = number * sign;
        ls.add(number);
    }

    /**
     * calculate the evaluation from the array.
     * @throws CalculatorError
     */
    public void Calculate() throws CalculatorError{
        Double first = null,second = null;
        char action = ' ';
        Object obj;
        for (int i=0;i<ls.size();i++){
            obj = ls.get(i);
            if (obj instanceof Double){
                if (first == null)
                {
                    first = (double)(obj);
                }
                else
                {
                    second = (double)(obj);
                    switch (action){
                        case '+':
                            first = first + second;
                            break;
                        case '/':
                            if (second != 0){
                                first = first/second;
                            }
                            else
                                throw new CalculatorError("diviation by zero");
                            break;
                        case '*':
                            first = first *second;
                            break;
                        case '-':
                            first = first -second;
                            break;
                        default:
                            throw new CalculatorError("Un know function");
                    }
                }
            }
            else if (obj instanceof Character){
                action = (char)(obj);
            }
        }
        System.out.printf("%f%n",first);
        result = first;
        status = true;
    }
}

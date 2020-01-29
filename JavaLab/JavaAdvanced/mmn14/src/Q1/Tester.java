package Q1;

public class Tester {
    /**
     * Array op person to have
     */
    static Person[] prArr =  { new Person(175,"Yehonathan","316304740"),
            new Person(180,"Eliraz","209015622"),
            new Person(170,"Jacob","014559761"),
            new Person(179,"Dave","756125478"),
            new Person(165,"Jannet","076855574"),
            new Person(179,"Dave","756125478"),
            new Person(185,"Kobi","153695478")};

    /**
     * make the tester
     */
    public static void main(String[] args) {
        System.out.printf("###### CREATING GROUP #####\n");
        SortedGroup<Person> group = new SortedGroup<Person>();
        System.out.printf("Group: %s%n",group.toString());

        System.out.printf("\n\n###### ADD PERSON #####\n");
        for (int i=0; i<prArr.length;i++){
            System.out.printf("Entering person: %s%n",prArr[i].toString());
            group.add(prArr[i]);
        }
        System.out.printf("Group: %s%n",group.toString());

        System.out.printf("\n\n###### REMOVE PERSON #####\n");
        System.out.printf("remove: %s\n",prArr[3].toString());
        System.out.printf("removed: %d\n",group.remove(prArr[3]));
        System.out.printf("Group: %s%n",group.toString());

        System.out.printf("\n\n###### REDUCE #####\n");
        Person rdPeson = new Person(175,"check","000000000");
        System.out.printf("reduce: %s\n",rdPeson.toString());
        System.out.printf("before: %s\n",group.toString());
        SortedGroup<Person> reduced = Q1_2.reduce(group,rdPeson);
        System.out.printf("reduced group: %s\n",reduced.toString());
        System.out.printf("afer: %s\n",group.toString());


        System.out.printf("\n\n###### END #####\n");
    }
}

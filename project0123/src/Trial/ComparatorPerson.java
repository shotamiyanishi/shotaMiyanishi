package Trial;
import java.util.*;
public class ComparatorPerson implements Comparator<Student>{
    public int compare(Student s1, Student s2) {
        if (s1.getDate().compareTo(s2.getDate()) == -1) {
            return -1;
        } else if (s1.getDate().compareTo(s2.getDate()) == 1) {
            return 1;
        } else {
            return 0;
        }
    }
}

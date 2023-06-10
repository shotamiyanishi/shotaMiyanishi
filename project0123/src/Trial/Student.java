package Trial;
import java.util.*;
import java.io.*;
import java.text.ParseException;
import java.text.SimpleDateFormat;


public class Student {
    private String birth;
    private Date date;
    private Calendar calendar;
    private static final SimpleDateFormat sDF  = new SimpleDateFormat("yyyy/MM/dd");;
    private int age;
    
    public Student (int age, String birth){
        this.age = age;
        this.birth = birth;
        date = null;
        calendar = Calendar.getInstance();
        try {
            date = sDF.parse(this.birth);
            calendar.setTime(date);
        } catch (ParseException e) {

        }
    }

    public int getAge() {
        return age;
    }

    public Calendar getCalendar() {
        return calendar;
    }

    public Date getDate() {
        return date;
    }

    public String toString() {
        String str = sDF.format(date);
        return str;
    }
}

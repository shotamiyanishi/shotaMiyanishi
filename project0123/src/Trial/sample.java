package Trial;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class sample {
    public  static void test() {
        try {
            BufferedReader br = new BufferedReader(new FileReader("project0123/src/Trial/hoge.txt"));
            br.readLine().split("");
        } catch (IOException e) {
            throw new HogeException("hogeエラー");
        } catch (NullPointerException e) {
            System.out.println("ヌルぽ");
        }
    }

    public static void main(String[] args) {
        test();
        System.out.println("bbbbbb");
    }
}

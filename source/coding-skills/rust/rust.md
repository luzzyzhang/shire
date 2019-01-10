# Rust programming language

## 简介

Rust 是一种系统编程语言。 它有着惊人的运行速度，能够防止段错误，并保证线程安全。

> Rust is a programming language that’s focused on safety, speed, and concurrency.
> Its design lets you create programs that have the performance and control of a low-level language, but with the powerful abstractions of a high-level language. 
> These properties make Rust suitable for programmers who have experience in languages like C and are looking for a safer alternative, 
> as well as those from languages like Python who are looking for ways to write code that performs better without sacrificing expressiveness.

## 特点

- 零开销抽象
- 转义语义
- 保证内存安全
- 线程无数据竞争
- 基于 trait 的泛型
- 模式匹配
- 类型推断
- 极小运行时
- 高效 C 绑定

## 实例

```rust
fn main() {
    let greetings = ["Hello", "Hola", "Bonjour",
                     "Ciao", "こんにちは", "안녕하세요",
                     "Cześć", "Olá", "Здравствуйте",
                     "Chào bạn", "您好", "Hallo",
                     "Hej", "Ahoj", "سلام"];

    for (num, greeting) in greetings.iter().enumerate() {
        print!("{} : ", greeting);
        match num {
            0 =>  println!("This code is editable and runnable!"),
            1 =>  println!("¡Este código es editable y ejecutable!"),
            2 =>  println!("Ce code est modifiable et exécutable !"),
            3 =>  println!("Questo codice è modificabile ed eseguibile!"),
            4 =>  println!("このコードは編集して実行出来ます！"),
            5 =>  println!("여기에서 코드를 수정하고 실행할 수 있습니다!"),
            6 =>  println!("Ten kod można edytować oraz uruchomić!"),
            7 =>  println!("Este código é editável e executável!"),
            8 =>  println!("Этот код можно отредактировать и запустить!"),
            9 =>  println!("Bạn có thể edit và run code trực tiếp!"),
            10 => println!("这段代码是可以编辑并且能够运行的！"),
            11 => println!("Dieser Code kann bearbeitet und ausgeführt werden!"),
            12 => println!("Den här koden kan redigeras och köras!"),
            13 => println!("Tento kód můžete upravit a spustit"),
            14 => println!("این کد قابلیت ویرایش و اجرا دارد!"),
            _ =>  {},
        }
    }
}

```
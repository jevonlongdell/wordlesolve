//use lazy_static::lazy_static;
//use regex::Regex;
use std::fs::File;
use std::path::Path;
use std::io::BufReader;
use std::io::stdin;
use std::io::prelude::*;
use std::collections::HashMap;
use std::collections::HashSet;
use libm::exp;
use libm::log2;
use std::cmp::min;
use itertools::izip;
//use text_io::read;


use std::hash::{Hash};


// fn is_five_letter_lowercase(text: &str) -> bool {
//     lazy_static! {
//         static ref RE: Regex = Regex::new("^[a-z][a-z][a-z][a-z][a-z]$").unwrap();
//     }
//     RE.is_match(text)
// }


//used to describe the info held about the mystery word
#[derive(PartialEq, Eq, PartialOrd, Ord, Hash)]
struct Info {
    green: Vec<char>,
    orange: Vec<Vec<char>>,
    grey: Vec<char>,
}

fn cal_resulting_entropy(guess: &str, possiblewords: &Vec<String>, words: &HashMap<String,f64>) -> f64 {
// Calculates the resulting entropy for a particular guess
// given the possible mystery words that are left

    let mut outcomes: HashMap<Info,Vec<&String>> = HashMap::new();

   // # for a given guess goes through all the posible mystery
   // # words and works out what the outcome would be for each
   // # of those possble mystery words
   // # returns a dict of which takes the orange,green,grey info
   // # an maps to a list of possible mystery words
    
    for mysteryword in possiblewords.iter(){


        let mut green: Vec<char> = ".....".chars().collect();
        let mut orange: Vec<Vec<char>> = Vec::new();
        for _k in 0..5 {
            orange.push(Vec::new());
        }
        let mut grey: Vec<char> = Vec::new();


        //fill out the greeen orange and grey for the guess and this mystery word
        for (wchar,greenchar,orange_item,guesschar) in izip!(mysteryword.chars(),green.iter_mut(),orange.iter_mut(),guess.chars()){
            if wchar == guesschar {
                *greenchar = guesschar ;
            } 
            else if mysteryword.contains(guesschar) {
                orange_item.push(guesschar);
            }
            grey.push(guesschar);
        }
    

        let info = Info{
            green: green.clone(),
            orange: orange.clone(),
            grey: grey.clone(),
        };

        //if info is in our list 
        if outcomes.contains_key(&info){
            outcomes.get_mut(&info).unwrap().push(mysteryword);
        } else {
            outcomes.insert(info, vec![mysteryword]);
        }
        //would be nice to do something like this if I could work out how
        // }
        // // match outcomes.get_mut(&info){
        //     Some(&mut words) => words.push(*mysteryword),
        //     None => outcomes.insert(info, vec![mysteryword]),
        // }


    }
    
    for (_info,wds) in outcomes.iter(){
        let mut poutcome = 0.0; //probablility of this outcome
        //flet mut Houtcome = 0.0; //entropy if this is the outcome
        for w in wds {
            poutcome += words.get(*w).unwrap();


        }


    }
    
    // for outcome in outcomes:
    //     #probability of a particular outcome
    //     #by summing the probabilities of the 
    //     #corresponding mysterywords
    //     poutcome=0
    //     Houtcome =0 # resulting entropy for if this is the outcome 
    //     for w in outcomes[outcome]:
    //         poutcome += words[w]
    //     for w in outcomes[outcome]:
    //         Houtcome += - words[w]/poutcome * math.log2( words[w] / poutcome) 


    //     H +=   poutcome*Houtcome
    // H


    return 1.0;
}


fn main() {


    //The "words" hash map stores the prior
    //probability for each word. 
    //we take the prior proability to be 
    //prob = exp(-k/3000) where k is the index of the word
    //in a list sorted by popularity
    //we read this list in from wordlist.txt 

        let wordlistpath = Path::new("wordlist.txt");
        let f = File::open(&wordlistpath).unwrap();
        let reader =  BufReader::new(f);

        //let mut wordlist : Vec<String> = [].to_vec();//Vec<String>;

        let mut words = HashMap::new();
        let mut probsum =0.0;
        for (k, line) in reader.lines().enumerate() {
            let p= exp((k as f64) / 3000.0);
            probsum += p;
            words.insert(line.unwrap(), p);
        }
        for (_, p) in words.iter_mut(){
            *p /= probsum;
        }


    // read in the green, orange and grey letters from stdin
        
        println!("Enter green letters. The ones you know for sure, put a dot for the ones you don't know (in form h.l..)");
        let mut greenstring =  String::new();
        stdin().read_line(&mut greenstring).unwrap();
        let mut greenstring = greenstring.trim();

        if greenstring=="" {
            greenstring= ".....";
        }
        assert_eq!(greenstring.len(),5);

        println!();
        println!();

        println!("Enter orange letters for each of the five letters, separated by four spaces, dots ignored");
        let mut orangestring = String::new();
        stdin().read_line(&mut orangestring).unwrap();
        let mut orangestring = orangestring.trim();
        if orangestring==""{
                orangestring=". . . . .";
        }
    
    
        println!();
        println!();
        println!("Enter letters that you have tried so fa (with no spaces between them, any order)\n just hit enter if there are none");
        let mut greystring = String::new();
        stdin().read_line(&mut greystring).unwrap();
        let greystring = greystring.trim();
        
    // turning user input in to datatype useful for 
    // subsequent computation
        let priorgreen = greenstring;
        
        let mut priororange: Vec<&str> = orangestring.split_whitespace().collect();
        for s in priororange.iter_mut(){
            if *s=="."{
                *s = "";
            }
        }
        assert_eq!(priororange.len(),5);

        let mut priorgrey = HashSet::new();
        for c in greystring.chars() {
            if !c.is_whitespace(){
                priorgrey.insert(c);
            }
        }
        // remove the green and orange letters from the grey ones
        for c in priorgreen.chars(){
            priorgrey.remove(&c);
        }
        for s in &priororange{
            for c in s.chars(){
                priorgrey.remove(&c);
                }
            }

        // make a list of possible solutions
        let mut possiblewords:Vec<&str> = Vec::new();

        'possiblewordsearch: 
        for (w,_) in words.iter(){
            
            for (wchar,gchar) in w.chars().zip( priorgreen.chars() ){
                //if it doesn't match green give up on this word
                if gchar!='.' &&  gchar!=wchar {
                    continue 'possiblewordsearch;
                }
                // if it has a grey letter give up
                if priorgrey.contains(&wchar){
                    continue 'possiblewordsearch;
                }
                
            }   

            let wordletters: HashSet<char> = w.chars().collect();
            for (o,wchar) in priororange.iter().zip(w.chars()){
                let wcharset = HashSet::from([wchar]);
                let wordletters_not_this_slot: HashSet<_> = wordletters.difference(&wcharset).collect();
                for ochar in o.chars(){
                    if !wordletters_not_this_slot.contains(&ochar){
                        continue 'possiblewordsearch
                    }
                    if wchar==ochar {
                        continue 'possiblewordsearch
                    }   
                }
                //orange leters are not green
                
            }
            
            possiblewords.push(w)

        }

        //Calculate current (initial) entropy 
        let N = possiblewords.len();

        if N==0{
            println!("No compatibile words found");
            return;
        }

        if N==1{
            println!("The answer is {}!",possiblewords[0]);
            return;
        }

        let nw= min(30,N);
        println!("Found {} possilbe words, the first {} are:",N,nw);
        for w in possiblewords.iter().take(nw){
            print!("{} ",w)
        }
        println!(); println!();
        

        let mut Hinit = 0.0;
        let mut probsum=0.0;
        for w in possiblewords.iter(){
            probsum+=words.get(w as &str).unwrap();
        }   
        for w in possiblewords.iter(){
            let p = words.get(w as &str).unwrap();
            Hinit -= p/probsum *log2(p/probsum);
        }
        
        {
        for wd in possiblewords.iter(){
            let w = words.get_mut(wd as &str).unwrap();
            *w /= probsum;
        }

        }
        
        println!("Initial entropy = {} bits",Hinit);







        println!("{:?} {:?} {:?} {:?} ",priorgreen, priororange,priorgrey,&mut possiblewords);
        
    
        
}

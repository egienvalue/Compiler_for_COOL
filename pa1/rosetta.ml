(* OCAML: Reverse-sort the lines from standard input *) 
let lines = ref [] in (* store the lines; a 'ref' is a mutable pointer *)
let t_visited = ref [] in
let p_visited = ref [] in
let edges = ref [] in
try
  while true do (* we'll read all the lines until something stops us *) 
    let line1 = (read_line()) in
    let line2 = (read_line()) in
    lines := line1 :: !lines (* read one line, add it to the list *)
    lines := line2 :: !lines
    edges := (line1, line2) :: !edges
    (* X :: Y makes a new list with X as the head element and Y as the rest *)
    (* !reference loads the current value of 'reference' *) 
    (* reference := value assigns value into reference *) 
  done (* read_line will raise an exception at the end of the file *) 
with _ -> begin (* until we reach the end of the file *) 
  let sorted = List.sort (* sort the linst *)
    (fun line_a line_b -> (* how do we compare two lines? *)
      compare line_b line_a) (* in reverse order! *) 
      (* (fun (argument) -> body) is an anonymous function *) 
    !lines (* the list we are sorting *)  
  in (* let ... in introduces a new local variable *) 
  List.iter print_endline sorted (* print them to standard output *)
  List.iter print_endline edges 
  (* List.iter applies the function 'print_endline' to every element 
   * in the list 'sorted' *) 
end 

-- HASKELL
import Data.List        -- contains sortBy

main = do 
        -- First, read all of stdin as one big string. 
        --   We use "a <- b" here instead of "let a = b" because
        --   getContents returns an "IO String" (as opposed to a "String"). 
        --   (This is an overly-simplified explanation.) 
        all_input_as_one_string <- getContents
        -- Next, split that string up into lines. 
        --   There is a convenient built-in function to do this for us.
        let all_input_as_lines = lines all_input_as_one_string
        -- Third, sort those lines. 
        --   How do we compare lines 'x' and 'y'? In reverse order! 
        let sorted = sortBy (\x -> \y -> compare y x) all_input_as_lines 
        -- Finally, print out the sorted list.
        mapM putStrLn sorted 
        -- We use mapM ("monadic map") here because the type of main
        -- should be "IO t" and using vanilla map yields type 
        -- [IO ()]. You can see Haskell's error message for that if
        -- you replace mapM by map above and try to recompile.

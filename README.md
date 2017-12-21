# commands

CMD
CMD i
('label', label_name)
('goto', label_name)


#if statement

IF STATEMENT THEN
    CMD
ENDIF

('if', 'cond')
('goto', label)

('if', not('cond'))
('goto', label)

```
    ('if_then', ('condition', '<>', ('int', 'a', 5), 0), 
        [
            ('assign', ('int', 'a', 6), ('expression', 0))
        ]
    )
    
    ('if', not(('a', '<>', 0)))
    ('goto', 'label1')
    CMDs
    ('label', 'label1')
    
    ...
    [condition],
    [ifcondgood],
    ...
    
        
    ('if_then', ('condition', '<>', ('int', 'a', 5), 0), 
        [   
            ('assign', ('int', 'a', 6), ('expression', 0)), 
            ('assign', ('int', 'a', 7), ('expression', 1)), 
            ('assign', ('int', 'a', 8), ('expression', 2))
        ]
    )
    
    ('if_else', ('condition', '<>', ('int', 'a', 5), 0), 
        [
            ('assign', ('int', 'a', 6), ('expression', 0))
        ], [
            ('assign', ('int', 'a', 8), ('expression', 4))
        ]
    )
    
    ('if', not(('a', '<>', 0)))
    ('goto', 'label1')
    CMDs
    ('goto', 'label2')
    ('label', 'label1')
    CMDs
    ('label', 'label2')
    ...
    [condition],
    [ifcondgood],
    [ifcondbad],
    ...
    
    

```
#if else statement

IF STATEMENT THEN
    CMD
ELSE
    CMD
ENDIF

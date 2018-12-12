import numpy as np
import matplotlib.pyplot as plt
import copy




class Data:
    
    PRINT_TABLE_SPACELEN = 16
    PRINT_TABLE_MAXLEN = 2
    PRINT_TABLE_MAXDEPTH = 50
    
    
    
    # ******************************************************** Initialization and Magic Methods ********************************************************

    def __init__(self, x, y, xname=None, yname=None, properties={}):
        """
        Initializes a Data object. It consists of x- and y-values and a set of properties, which is a dictionairy of int-dict pairs.
        
        Parameters
        ----------
        x: array_like or a number (float, int)
            The x-values of the data. The dimension of x must be 0 or 1.
            
        y: array_like or a number (float, int)
            The y-values of the data. y must be of shape (*, len(x)).
        
        xname: str, optional
            A string, that describes the x-values. Default is 'x'.
            
        yname: str, optional
            A string, that describes the y-values. Default is 'y'.
        
        properties: dictionary, optional
            A dictionary containing int-dictionary pairs, each int corresponds to the y-arrays along the first axis of y. The dictionary must not have more keys than y.shape[0]. The inner dictionaries can contain arbitrary (dict allowed) keys and values, whatever describes the data best. Default is an empty dictionairy properties={}, which is filled with int:None pairs upon Object creation.
            
        
        
        
        Raises
        ------
        TypeError
            If x or y are not mutable arrays or are not numbers.
        
        ValueError
            If y.shape[1] is not equal to len(x) or properties have more keys than y.shape[0] or one of the keys in properties is not int or one of the keys in properties is larger than y.shape[0]-1 (the keys shall correspondingly enumerate through the first axis of y starting from 0 in order to have a sound assignment of properties).
            
        """
        
        
        
        if type(x) not in (np.ndarray, list, float, int):
            raise TypeError("x must be of type np.ndarray, float or int.")
        
        if type(y) not in (np.ndarray, list, float, int):
            raise TypeError("y must be of type np.ndarray, float or int.")
        
        x = np.array(x)
        y = np.array(y)
        
        if x.shape != () and y.shape != ():
            if len(x) > 0:
                if y.shape[1] != len(x):
                    raise ValueError("Expected y to be of shape (*, %d), but has shape (*, %d)."%(len(x), y.shape[1]))
                if len(x.shape) > 1:
                    raise ValueError("The dimension of x must not exceed 1.")
            else:
                if len(y.shape) > 1:
                    raise ValueError("Expected y to be a 1-dimensional array or a number, since x is a number.")
        
        elif x.shape != () and y.shape == ():
            raise ValueError("Expected y to be of shape (*, %d), but it has shape %s."%(len(x), str(y.shape)))
            
        elif x.shape == () and len(y.shape) > 1:
            raise ValueError("y must have shape (1,), but has shape %s."%(str(y.shape)))

        
        if y.shape != () and len(properties) > y.shape[0]:
            raise ValueError("The number of keys in properties must not be larger than y.shape[0] = %d."%y.shape[0])
        elif y.shape == () and len(properties) > 1:
            raise ValueError("As y is a number, only a single or no propoerty at all are allowed for properties.")
        
        for key in properties:
            if type(key) != int:
                raise ValueError("All keys in properties must be of type int.")
            if y.shape != () and key >= y.shape[0]:
                raise ValueError("Found key in properties %d >= y.shape[0] = %d. Key values must be smaller than y.shape[0]."%(key, y.shape[0]))
            elif y.shape == () and key > 0:
                raise ValueError("As y is a number, the only allowed key for properties is 0.")
            elif type(properties[key]) != dict and properties[key] != None:
                raise TypeError("The values of properties must be of type dict or None.")
        
            
        if type(xname) not in (None, str):
            raise TypeError("xname must be None or of type str.")
        
        if type(xname) not in (None, str):
            raise TypeError("xname must be None or of type str.")
        
            
        if y.shape == ():
            self.length = 1
        else:
            self.length = len(y)
            
        if x.shape == () and y.shape == ():
            self.dtype = 'num-num'
        elif x.shape == () and y.shape != ():
            self.dtype = 'num-arr'
        else:
            self.dtype = 'arr-arr'
        
        self.x = copy.deepcopy(np.array(x))
        self.y = copy.deepcopy(np.array(y))
        
        self.xshape = x.shape
        self.yshape = y.shape
        
        if xname != None:
            self.xname = xname
        else:
            self.xname = 'x'
        if yname != None:
            self.yname = yname
        else:
            self.yname = 'y'
        
        self.properties = copy.deepcopy(properties)
        self.properties_keys = properties.keys()
        self.properties_maxlen = 0
        

        for i in range(self.length):

            if i not in self.properties_keys:
                self.properties[i] = None
            
            if self.properties[i] != None and len(self.properties[i]) > self.properties_maxlen:
                self.properties_maxlen = len(self.properties[i])

                
        self.properties_keys = self.properties.keys()
    
    
    
    
    def __len__(self):
        """
        Length of the Data. If y is a number, the length is one, otherwise the length equals the length of the y-array (first axis).
        
        Returns
        -------
        length: int
            The length of the Data, i.e. 1 if y is a number or the length of the first axis of the y-array if y is array-like.
        """
        return self.length


    def __str__(self):
        
        """
        String representation of the Data in table format.
        
        Returns
        -------
        string: str 
            Data represented in table format.
        """
        
        print('\n')
        
        if self.dtype == 'num-num':
            string = self.get_table_numnum()
        elif self.dtype == 'num-arr':
            string = self.get_table_numarr()
        elif self.dtype == 'arr-arr':
            string = self.get_table_arrarr()
            
        
        print('\n')
        
        return string
    
    
    
    
    def __getitem__(self, key):
        """
        Returns the y-arrays as indexed. Indexing works similar as with lists and numpy arrays.
        
        Parameters
        ----------
            key: int or slice
                The index/indices of the y-arrays to be returned.
                
        Raises
        ------
            IndexError
                If key is integer and key >= Data.length or key < -Data.length.
        """
        
        if type(key) == int:
            if key >= self.length or key < -self.length:
                raise IndexError("Index %d is out of range for Data with length %d."%(key, self.length))
                
        return self.y[key]
          
          
          
                
    def __setitem__(self, key, value):
        """
        Sets the y-arrays as indexed. Indexing works similar as with lists and numpy arrays.
        
        Parameters
        ----------
            key: int or slice
                The index/indices of the y-arrays to be set.
                
            value: int/float or array-like
                A number or an array (1 or 2 dimensional) with values to be written to the indexed y-arrays of Data.
                
        Raises
        ------
            IndexError
                If key is integer and key >= Data.length or key < -Data.length.
        """
        
        if type(key) == int:
            if key >= self.length or key < -self.length:
                raise IndexError("Index %d is out of range for Data with length %d."%(key, self.length))
                
                
        self.y[key] = value
        
    
    
    
    def __delitem__(self, key):
        """
        Deletes the y-arrays and corresponding properties as indexed. Indexing works similar as with lists and numpy arrays.
        
        Parameters
        ----------
            key: int or slice
                The index/indices to be deleted.
                
        Raises
        ------
            IndexError
                If key is integer and key >= Data.length or key < -Data.length.
        """
        
        if type(key) == int:
            if key >= self.length or key < -self.length:
                raise IndexError("Index %d is out of range for Data with length %d."%(key, self.length))
            
        self.y = np.delete(self.y, key, axis=0)
        self.length = len(self.y)
        
        if type(key) == int:
            del(self.properties[key])
        else:
            for i in np.arange(self.length)[key][::-1]:
                del(self.properties[i])
        
        newproperties = {}
        newproperties_maxlen = 0
        count = 0
        for k in self.properties:
            newproperties[count] = self.properties[k]
            if newproperties[count] != None and len(newproperties[count]) > newproperties_maxlen:
                newproperties_maxlen = len(newproperties[count])
            count += 1
        self.properties = newproperties
        self.properties_maxlen = newproperties_maxlen
            
        
        
    

    # ******************************************************** Standard I/O *******************************************************
    
        
    def get_table_numnum(self):
        
        """
        Method for printing the Data in table format, if self.dtype = 'num-num' (x and y are numbers).
        
        Returns
        -------
        string: str
            The Data represented in table format.
        """
        
        
        spacelen = Data.PRINT_TABLE_SPACELEN
        maxlen = Data.PRINT_TABLE_MAXLEN
        spaces = spacelen*' '
       
        hypherlen = 0
        
        string = ' x' + spaces + '|'
        string += ' y' + spaces + '\n'
        
        hypherlen = len(string)
        
        string += hypherlen*'-' + '\n'
        
        if len(self.properties) != 0:
            if self.properties[0] != None:
                for key in self.properties[0]:
                
                    string += (spacelen+2)*' ' + '|'
                    propstring = ' ' + str(key) + ':' + str(self.properties[0][key])
                    string += propstring + (spacelen-len(propstring)+2)*' ' + '\n'
                string += '-'*hypherlen + '\n'
        
            
        
        
        xstring = ' %g'%self.x
        ystring = ' %g'%self.y
        
        string += xstring + (spacelen - len(xstring) + 2)*' ' + '|'
        string += ystring + (spacelen - len(ystring) + 2)*' ' + '\n'
        string += hypherlen*'-'
        
        prestring = self.xname + (spacelen-len(self.xname)+2)*' ' + '|' + self.yname+ '\n'
        prestring += hypherlen*'-' + '\n' + hypherlen*'-' + '\n'
        
        return prestring + string
    
    
    def get_table_numarr(self):
        
        """
        Method for printing the Data in table format, if self.dtype = 'num-arr' (x is a number and y is array-like).
        
        Returns
        -------
        string: str
            The Data represented in table format.
        """
        
        spacelen = Data.PRINT_TABLE_SPACELEN
        maxlen = Data.PRINT_TABLE_MAXLEN
        spaces = spacelen*' '
        
        hypherlen = 0
        
        
        
        
        string = ' x' + spaces + '|'
        
        for i in range(self.length-1):
            if i > maxlen:
                string += ' ... ' + '|'
                break
            string += ' y[%d,:]'%i + spaces + '|'
            
        string += ' y[%d,:]\n'%(self.length-1)
        
        hypherlen = len(string) + spacelen
        string += '-'*hypherlen
        
        for i in range(self.properties_maxlen):
            

            
            string += '\n' + ' '*2 + spaces + '|'
            
            for j in range(self.length-1):
                if j > maxlen:
                    string += ' ... '  + '|'
                    break
                
                if self.properties[j] == None:
                    string += ' NoProp' + spaces + '|' 
                else:
                    if i >= len(self.properties[j]):
                        string += ' NoProp' + spaces + '|'
                    else:
                        propstring = ' ' + str(list(self.properties[j].keys())[i]) + ':' + str(self.properties[j][list(self.properties[j].keys())[i]])
                        string += propstring + (spacelen-len(propstring) + 7)*' ' + '|'
            
            
            j = self.length-1
            
            if self.properties[j] == None:
                string += ' NoProp' + spaces + '\n'
            else:
                if i >= len(self.properties[j]):
                    string += ' NoProp' + spaces + '\n'
                else:
                    propstring = ' ' + str(list(self.properties[j].keys())[i]) + ':' + str(self.properties[j][list(self.properties[j].keys())[i]])
                    string += propstring + (spacelen-len(propstring) + 7)*' ' + '\n'
            
        string += hypherlen*'-' + '\n'
        
        if self.properties_maxlen == 0:
            string += '\n'
        
        xstring = ' %g'%self.x
        string += xstring + (spacelen-len(xstring)+2)*' ' + '|'
        
        for i in range(self.length-1):
            if i > maxlen:
                string += ' ... ' + '|'
                break
            ystring = ' %g'%self.y[i]
            string += ystring + (spacelen-len(ystring)+7)*' ' + '|'
        
        i = self.length-1 
        ystring = ' %g'%self.y[i]
        string += ystring + (spacelen-len(ystring)+7)*' ' + '\n'
        
        
        string += '-'*hypherlen
        
        prestring = self.xname + (spacelen-len(self.xname)+2)*' ' + '|' + self.yname+ '\n'
        prestring += hypherlen*'-' + '\n' + hypherlen*'-' + '\n'
        
        
        return prestring + string
    
    
    def get_table_arrarr(self):
        
        """
        Method for printing the Data in table format, if self.dtype = 'num-arr' (x and y are array-like).
        
        Returns
        -------
        string: str
            The Data represented in table format.
        """
        
        spacelen = Data.PRINT_TABLE_SPACELEN
        maxlen = Data.PRINT_TABLE_MAXLEN
        maxdepth = Data.PRINT_TABLE_MAXDEPTH
        spaces = spacelen*' '
        
        
        hypherlen = 0
        
        string = ' x[:]' + spaces + '|'
        
        for i in range(self.length-1):
            if i > maxlen:
                string += ' ... ' + '|'
                break
            string += ' y[%d,:]'%i + spaces + '|'
            
        string += ' y[%d,:]\n'%(self.length-1)
        
        hypherlen = len(string) + spacelen
        string += '-'*hypherlen
        
        
        for i in range(self.properties_maxlen):
            

            
            string += '\n' + ' '*5 + spaces + '|'
            
            for j in range(self.length-1):
                if j > maxlen:
                    string += ' ... '  + '|'
                    break
                
                if self.properties[j] == None:
                    string += ' NoProp' + spaces + '|' 
                else:
                    if i >= len(self.properties[j]):
                        string += ' NoProp' + spaces + '|'
                    else:
                        propstring = ' ' + str(list(self.properties[j].keys())[i]) + ':' + str(self.properties[j][list(self.properties[j].keys())[i]])
                        string += propstring + (spacelen-len(propstring) + 7)*' ' + '|'
            
            
            j = self.length-1
            
            if self.properties[j] == None:
                string += ' NoProp' + spaces + '\n'
            else:
                if i >= len(self.properties[j]):
                    string += ' NoProp' + spaces + '\n'
                else:
                    propstring = ' ' + str(list(self.properties[j].keys())[i]) + ':' + str(self.properties[j][list(self.properties[j].keys())[i]])
                    string += propstring + (spacelen-len(propstring) + 7)*' ' + '\n'
            
        string += hypherlen*'-' + '\n'
        
        if self.properties_maxlen == 0:
            string += '\n'
        
        
        for i in range(len(self.x)-1):
            
            if i > maxdepth:
                string += '-'*hypherlen + '\n\n' + (hypherlen//2-4)*' ' + '......' + '\n' + '-'*hypherlen + '\n'
                break
            
            xstring = ' %g'%self.x[i]
            string += xstring + (spacelen-len(xstring)+5)*' ' + '|'
        
            for j in range(self.length-1):
                if j > maxlen:
                    string += ' ... ' + '|'
                    break
                ystring = ' %g'%self.y[j][i]
                string += ystring + (spacelen-len(ystring)+7)*' ' + '|'
        
            j = self.length-1 
            ystring = ' %g'%self.y[j][i]
            string += ystring + (spacelen-len(ystring)+7)*' ' + '\n'
        
        i = len(self.x)-1
        
        xstring = ' %g'%self.x[i]
        string += xstring + (spacelen-len(xstring)+5)*' ' + '|'
        
        for j in range(self.length-1):
            if j > maxlen:
                string += ' ... ' + '|'
                break
            ystring = ' %g'%self.y[j][i]
            string += ystring + (spacelen-len(ystring)+7)*' ' + '|'
    
        j = self.length-1 
        ystring = ' %g'%self.y[j][i]
        string += ystring + (spacelen-len(ystring)+7)*' ' + '\n'
        
        string += '-'*hypherlen
        
        prestring = self.xname.upper() + (spacelen-len(self.xname)+5)*' ' + '|' + self.yname.upper() + '\n'
        prestring += hypherlen*'-' + '\n' + hypherlen*'-' + '\n'
        
        return prestring + string
    
    

    # ******************************************************** Setters *******************************************************

    def set_x(self, x):
        
        if type(self.x) == np.ndarray:
            if type(x) not in (np.ndarray, list):
                raise TypeError("x must be array-like, i.e. np.ndarray or list.")
            if np.array(x).shape != self.x.shape:
                raise ValueError("x with shape %s does not fit to the structure of the data. Must be of shape %s."%(str(np.array(x).shape), str(self.x.shape)))
        
        if type(self.x) in (int, float):
            if type(x) not in (int, float):
                raise TypeError("x must be a number, i.e. int or float.")
        
        if type(self.x) in (int, float):
            self.x = x
        else:
            self.x = copy.deepcopy(np.array(x))
            
            
        
    def set_y(self, y, *index):
        
        if type(self.y) == np.ndarray:
            if type(y) not in (np.ndarray, list):
                raise TypeError("y must be array-like, i.e. np.ndarray or list.")
            if len(index) == 0:
                if np.array(y).shape != self.y.shape:
                    raise ValueError("y with shape %s does not fit to the structure of the data. Must be of shape %s."%(str(np.array(y).shape), str(self.y.shape)))
            else:
                if np.array(y).shape != self.x.shape:
                    raise ValueError("y with shape %s does not fit to the structure of the data. Must be of shape %s."%(str(np.array(y).shape), str(self.x.shape)))
                
        
        if type(self.y) in (int, float):
            if type(y) not in (int, float):
                raise TypeError("y must be a number, i.e. int or float.")
        
        
        if type(self.y) in (int, float):
            self.y = y

        if len(index) == 0:
            self.y = copy.deepcopy(np.array(y))
        else:
            for i in index:
                if i > self.length:
                    raise IndexError("Index %d is out of range for Data with length %d."%(i, self.length))
                if len(self.yshape) == 1:
                    self.y[i] = y
                else:
                    self.y[i,:] = copy.deepcopy(np.array(y))
            



    def set_properties(self, properties, *index):
        if type(properties) != dict:
            raise TypeError("properties must be a dictionary.")
        
        if len(index) == 0:
            
            existing_keys = []
            for key in properties:
                
                if type(key) != int:
                    raise TypeError("Any key in properties must be of type int.")
                if type(properties[key]) != dict and properties[key] != None:
                    raise TypeError("Any value in properties must be of type dict or None.")
                if key >= self.length:
                    raise IndexError("The key  %d in properties is out of range for Data with length %d."%(key, self.length))
                
                existing_keys.append(key)
            
                self.properties[key] = properties[key]
                if len(properties[key]) > self.properties_maxlen:
                    self.properties_maxlen = len(properties[key])
            
            for i in range(self.length):
                if i not in existing_keys:
                    self.properties[i] = None
        
        else:
            
            for i in index:
                if i >= self.length:
                    raise IndexError("Index %d is out of range for Data with length %d."%(i, self.length))
                self.properties[i] = properties
                if len(properties) > self.properties_maxlen:
                    self.properties_maxlen = len(properties)
                

    def set_xname(self, xname):
        if type(xname) != str:
            raise TypeError("xname must be of type str.")
        self.xname = xname
    

    def set_yname(self, yname):
        if type(yname) != str:
            raise TypeError("yname must be of type str.")
        self.yname = yname    
                

    # ******************************************************** Getters *******************************************************

    def get_x(self):
        """
        Get the x-array of the Data.
        
        Returns
        -------
            x: number or numpy array
                The x-values in Data.
        """
        return x

    
    def get_y(self, *index):
        """
        Get the y-array of the Data for specified indices.
        
        Parameters
        ----------
        *index: zero or more ints
            The indices of the y-columns to return.
        
        Returns
        -------
            y: number or numpy array
                The y-values in Data for *index. If *index is not specified, the whole array of values is returned.
        """
        
        
        if np.any(np.array(index) > self.length-1):
            raise IndexError("At least one index is out of range for Data with length %d."%self.length)
        
        if len(index) == 0:
            return self.y
        else:
            if type(self.y) in (int, float):
                raise IndexError("Cannot grab index of Data's y. It is a number.")
            if len(index) == 1:
                return np.take(self.y, index, axis=0)[0]
            else:
                return np.take(self.y, index, axis=0)


    def get_properties(self, *index):
        """
        Get the properties of the Data for specified indices.
        
        Parameters
        ----------
        *index: zero or more ints
            The indices of the y-columns to return.
        
        Returns
        -------
            props: dict of int-dict pairs
                The properties for th columns in Data specified by *index. If *index is not specified, the whole proeprties-dict is returned.
        """
        
        if np.any(np.array(index) > self.length-1):
            raise IndexError("At least one index is out of range for Data with length %d."%self.length)
        
        if len(index) == 0:
            return self.properties
        p = {}
        for i in index:
            p[i] = self.properties[i]
        return p
    
    def get_xname(self):
        return self.xname
    
    def get_yname(self):
        return self.yname
    
    
    # ******************************************************** Appending *******************************************************


    def append(self, y, properties=[], axis=0):
        """
        Appends y to the data along the specified axis. It uses the methods Data.append_numnum_numarr and Data.append_arrarr.
        
        Parameters
        ----------
            y: number or array-like
                Values to append to the Data.y (axis=0) or Data.x and Data.y (axis=0)
                
            properties: list of dicts, optional
                Properties for the new y-columns (axis=0) or new properties for y-columns (axis=1). Default is [].
                
            axis: int, optional
                Axis along which the values shall be appended. axis=0 means, that new y columns are appended, for axis=1 new rows are created. Default is 0.
        """
        
        if self.dtype == 'num-num' or self.dtype == 'num_arr':
            self.append_numnum_numarr(y, properties=properties, axis=axis)
        elif self.dtype == 'arr-arr':
            self.append_arrarr(y, properties=properties, axis=axis)
    
    
    
    
    def append_numnum_numarr(self, y, properties=[], axis=0):
        """
        Appends y to the data along the specified axis for the case that Data.dtype='num_num' or ='num-arr'.
        
        Parameters
        ----------
            y: number or array-like
                Values to append to the Data.y (axis=0) or Data.x and Data.y (axis=0)
                
            properties: list of dicts, optional
                Properties for the new y-columns (axis=0) or new properties for y-columns (axis=1). Default is [].
                
            axis: int, optional
                Axis along which the values shall be appended. axis=0 means, that new y columns are appended, for axis=1 new rows are created. Default is 0.
                
        
        Raises
        ------
            ValueError
                If axis not 0 or 1 or if the shapes of the inputs are not suited for appending along the specified axis.
            
            TypeError
                If the input has not the correct type.
        """
        
        if axis == 0:
            if type(y) in (float,int):
                if len(properties) > 1:
                    raise ValueError("properties must not contain more than 1 dict.")
                
            elif type(y) in (list, np.ndarray):
                y = np.array(y)
                if len(y.shape) != 1:
                    raise ValueError("y must have shape (*,), but has shape %s."%str(y.shape))
                if len(properties) > y.shape[0]:
                    raise ValueError("properties must not contain more than %d dicts."%y.shape[0])
                
            
            else:
                raise TypeError("y must be a number or one-dimensional array-like.")
                
            
            self.y = np.append(self.y, y)
            proplen = self.length-1
            
            for i in range(len(properties)):
                if type(properties[i]) != dict:
                    raise TypeError("properties must contain elements of type dict.")
                self.properties[self.length+i] = properties[i]
                if len(properties[i]) > self.properties_maxlen:
                    self.properties_maxlen = len(properties[i])
                proplen = self.length + i
            
            if type(y) in (int, float):
                self.length += 1
            else:
                self.length += len(y)
                
            for i in range(proplen+1, self.length):
                self.properties[i] = None
            
            self.dtype = 'num-arr'
           
        elif axis == 1:
            if type(y) in (list, np.ndarray):
                y = np.array(y)
                
                if len(properties) not in (0, self.length):
                    raise ValueError("The length of properties must be 0 or %d but has length %d."%(self.length, len(properties)))
                
                if len(y.shape) == 2:
                    if y.shape[1] != self.length+1:
                        raise ValueError("Second axis of y must be of length %d, but has length %d."%(y.shape[1], self.length+1))
                    
                    self.y = np.append(self.y.reshape(self.length,1), y[:,1::], axis=1)
                    self.x = np.append(self.x, y[:,0])
                    
                    
                elif len(y.shape) == 1:
                    if y.shape[0] != self.length+1:
                        raise ValueError("First axis of y must be of length %d, but has length %d."%(y.shape[0], self.length+1))
                    
                    
                    self.y = np.append(self.y.reshape(self.length,1), y[1::].reshape(self.length, 1), axis=1)
                    self.x = np.append(self.x, y[0])
                    
                else:
                    raise ValueError("y must have shape (%d,) or (*,%d), but is of shape %s."%(self.length+1, self.length+1, str(y.shape)))
                
                proplen = 0
                for i in range(len(properties)):
                    if type(properties[i]) != dict:
                        raise TypeError("properties must contain elements of type dict.")
                    self.properties[i] = properties[i]
                    if len(properties[i]) > proplen:
                        proplen = len(properties[i])
                
                if proplen > self.properties_maxlen:
                    self.properties_maxlen = proplen
                
            else:
                raise TypeError("y must be array-like.")
            
            
            
            
            self.dtype = 'arr-arr'
        
        else:
            raise ValueError("axis must be 0 or 1.")
           
           
           
           
            
    def append_arrarr(self, y, properties=[], axis=0):
        """
        Appends y to the data along the specified axis for the case that Data.dtype='num_arr'.
        
        Parameters
        ----------
            y: number or array-like
                Values to append to the Data.y (axis=0) or Data.x and Data.y (axis=0)
                
            properties: list of dicts, optional
                Properties for the new y-columns (axis=0) or new properties for y-columns (axis=1). Default is [].
                
            axis: int, optional
                Axis along which the values shall be appended. axis=0 means, that new y columns are appended, for axis=1 new rows are created. Default is 0.
                
        
        Raises
        ------
            ValueError
                If axis not 0 or 1 or if the shapes of the inputs are not suited for appending along the specified axis.
            
            TypeError
                If the input has not the correct type.
        """
        
        
        if type(y) not in (list, np.ndarray):
            raise TypeError("y must be array-like.")
        y = np.array(y)
        
        if axis == 0:
            
            if len(y.shape) == 2:
                if len(properties) > y.shape[0]:
                    raise ValueError("properties must not contain more than %d dicts."%y.shape[0])
                
                if y.shape[1] != len(self.x):
                    raise ValueError("The second axis of y must have length %d, but has length %d."%(len(self.x), y.shape[1]))
                
                self.y = np.append(self.y, y, axis=0)
                
            elif len(y.shape) == 1:
                if len(properties) > 1:
                    raise ValueError("properties must have length 0 or 1, but has length %d."%(len(properties)))
                
                
                if y.shape[0] != len(self.x):
                    raise ValueError("y must have length %d, but has length %d."%(len(self.x), y.shape[0]))
                
                
                self.y = np.append(self.y, y.reshape(1, len(self.x)), axis=0)
                
            else:
                raise ValueError("y must be of shape (%d,) or (*,%d), but has shape %s."%(len(self.x), len(self.x), str(y.shape)))
            
            proplen = self.length-1
            for i in range(len(properties)):
                if type(properties[i]) != dict:
                    raise TypeError("properties must contain elements of type dict.")
                self.properties[self.length+i] = properties[i]
                if len(properties[i]) > self.properties_maxlen:
                    self.properties_maxlen = len(properties[i])
                proplen = self.length + i
                
            if len(y.shape) == 2:
                self.length += self.y.shape[1]
            else:
                self.length += 1
            
            for i in range(proplen+1, self.length):
                self.properties[i] = None
            
            
            
        elif axis == 1:
            
            if len(properties) not in (0, self.length):
                raise ValueError("properties must not contain 0 or %d dicts."%self.length)
            
            if len(y.shape) == 2:
                
                if y.shape[1] != self.length+1:
                    raise ValueError("The second axis of y must have length %d, but has length %d."%(self.length+1, y.shape[1]))
                
                
                self.y = np.append(self.y, y[:,1::], axis=1)
                self.x = np.append(self.x, y[:,0])
                
            elif len(y.shape) == 1:
                
                if y.shape[0] != self.length+1:
                    raise ValueError("y must have length %d, but has length %d."%(self.length+1, y.shape[0]))
                
                
                self.y = np.append(self.y, y[1::].reshape(self.length, 1), axis=1)
                self.x = np.append(self.x, y[0])
                
            else:
                raise ValueError("y must be of shape (%d,) or (*,%d), but has shape %s."%(self.length+1, self.length+1, str(y.shape)))
            
            proplen = 0
            for i in range(len(properties)):
                if type(properties[i]) != dict:
                    raise TypeError("properties must contain elements of type dict.")
                self.properties[i] = properties[i]
                if len(properties[i]) > proplen:
                    proplen = len(properties[i])
            
            if proplen > self.properties_maxlen:
                self.properties_maxlen = proplen
            
        else:
            raise ValueError("axis must be 0 or 1.")
            
            
            
            
            
            
    # ******************************************************** Numerical Manupulations *******************************************************
    
    def interp_nan(self, *index):
        """
        Interpolate out nans in the Data. The columns indícated by *index will be interpolated. If *index is not specified, all columns will be interpolated.
        
        
        Parameters
        ----------
            *index: zero or more ints.
                The columns to be treated.
            
        Raises
        ------
            ValueError
                If an index is not smaller than Data.length.
        
        """
        
        if np.any(np.array(index) >= self.length):
            raise IndexError("At least one index is out of range for Data with length %d."%self.length)
        
        if len(index) == 0:
            for i in range(self.length):
                barray = ~np.isnan(self.y[i,:])
                self.y[i,:] = np.interp(self.x, self.x[barray], self.y[i,barray])
        else:
            for i in range(index):
                if i >= self.length:
                    raise ValueError("At least one index is out of range for Data with length %d."%self.length)
                barray = ~np.isnan(self.y[i,:])
                self.y[i,:] = np.interp(self.x, self.x[barray], self.y[i,barray])
                
                
                
    def interp_nonpositive(self, *index):
        """
        Interpolate out nonpositive numbers (<= 0) in the Data. The columns indícated by *index will be interpolated. If *index is not specified, all columns will be interpolated.
        
        
        Parameters
        ----------
            *index: zero or more ints.
                The columns to be treated.
            
        Raises
        ------
            ValueError
                If an index is not smaller than Data.length.
        
        """
        
        if np.any(np.array(index) >= self.length):
            raise IndexError("At least one index is out of range for Data with length %d."%self.length)
        
        if len(index) == 0:
            for i in range(self.length):
                barray = self.y[i,:] > 0
                self.y[i,:] = np.interp(self.x, self.x[barray], self.y[i,barray])
        else:
            for i in index:
                if i >= self.length:
                    raise ValueError("At least one index is out of range for Data with length %d."%self.length)
                barray = self.y[i,:] > 0
                self.y[i,:] = np.interp(self.x, self.x[barray], self.y[i,barray])
                
                
    def interp_to(self, x):
        """
        Interpolate the Data to array or number x. The x- and y-values will be resetted.
        
        
        Parameters
        ----------
            x: number or array-like.
                The new x-value(s).
            
        Raises
        ------
            TypeError
                If x is not a number or not array-like.
        
        """
        if type(x) not in (int, float, list, np.ndarray):
            raise TypeError("x must be a number (int/float) or array-like.")
        
        newy = np.zeros((self.length, len(x)))
        for i in range(self.length):
            newy[i,:] = np.interp(x, self.x, self.y[i,:])
        self.x = x
        self.y = newy
        
        
        
    def norm_max(self):
        """
        Normalize the data with respect to the maximum value.
        """
        maxval = self.stat_max(glob=True)
        self.y /= maxval
        

    def norm_min(self):
        """
        Normalize the data with respect to the maximum value.
        """
        minval = self.stat_min(glob=True)
        self.y /= minval
        
            
            
    # ******************************************************** Numerics *******************************************************
    
            

    # ******************************************************** Statistics *******************************************************

    def stat_max(self, *index, glob=False):
        """
        Find the maxima of the columns specified by *index or among the specified *index (if glob=True).
        
        Parameters
        ----------
            *index: zero or more ints.
                The indices specifying the columns of which the maxima shall be found.
                
            glob: bool, optional
                If glob=False an array containing the maximum values of the columns specified by *index is returned. Otherwise the maximum among those columns is returned.
            
        Returns
        -------
            maxima: number or array-like
                The maxima of the columns specified by *index. Has shape (len(index),:) or is a number if only one index is specified.
                
            
        Raises
        ------
            ValueError
                If an index is not smaller than Data.length.
        """
        
        if np.any(np.array(index) >= self.length):
            raise IndexError("At least one index is out of range for Data with length %d."%self.length)
        
        if len(index) == 0:
            if glob:
                return self.y.max()
            else:
                return self.y.max(axis=1)
        
        elif len(index) == 1:
            return self.y[index[0],:].max()
        
        else:
            maxima = np.zeros(len(index))
            count = 0
            for i in index:
                if type(self.y) in (int, float):
                    maxima[count] = self.y
                elif len(self.y.shape) == 1:
                    maxima[count] = self.y[i].max()
                else:
                    maxima[count] = self.y[i,:].max()
                count += 1
            if glob:
                return maxima.max()
            else:
                return maxima
            
            
            
        

    def stat_min(self, *index, glob=False):
        """
        Find the minima of the columns specified by *index.
        
        Parameters
        ----------
            *index: zero or more ints.
                The indices specifying the columns of which the minima shall be found.
                
            glob: bool, optional
                If glob=False an array containing the minimum values of the columns specified by *index is returned. Otherwise the minimum among those columns is returned.
            
        Returns
        -------
            minima: number or array-like
                The minima of the columns specified by *index. Has shape (len(index),:) or is a number if only one index is specified.
                
            
        Raises
        ------
            ValueError
                If an index is not smaller than Data.length.
        """

        if np.any(np.array(index) >= self.length):
            raise IndexError("At least one index is out of range for Data with length %d."%self.length)
        
        if len(index) == 0:
            if glob:
                return self.y.min()
            else:
                return self.y.min(axis=1)
        
        elif len(index) == 1:
            return self.y[index[0],:].min()
        
        else:
            minima = np.zeros(len(index))
            count = 0
            for i in index:
                if type(self.y) in (int, float):
                    minima[count] = self.y
                elif len(self.y.shape) == 1:
                    minima[count] = self.y[i].min()
                else:
                    minima[count] = self.y[i,:].min()
                count += 1
            if glob:
                return minima.min()
            else:
                return minima
        
        
        
    def stat_mean(self, *index, glob=False):
        """
        Find the means of the columns specified by *index.
        
        Parameters
        ----------
            *index: zero or more ints.
                The indices specifying the columns of which the means shall be found.
            
        Returns
        -------
            means: number or array-like
                The means of the columns specified by *index. Has shape (len(index),:) or is a number if only one index is specified.
                
            glob: bool, optional
                If glob=False an array containing the mean values of the columns specified by *index is returned. Otherwise the mean among those columns is returned.
                
            
        Raises
        ------
            ValueError
                If an index is not smaller than Data.length.
        """

        if np.any(np.array(index) >= self.length):
            raise IndexError("At least one index is out of range for Data with length %d."%self.length)
        
        if len(index) == 0:
            if glob:
                return np.mean(self.y)
            else:
                return np.mean(self.y, axis=1)
        
        elif len(index) == 1:
            return np.mean(self.y[index[0],:])
        
        else:
            means = np.zeros(len(index))
            count = 0
            for i in index:
                if type(self.y) in (int, float):
                    means[count] = self.y
                elif len(self.y.shape) == 1:
                    means[count] = np.mean(self.y[i])
                else:
                    means[count] = np.mean(self.y[i,:])
                count += 1
            if glob:
                return np.mean(means)
            else:
                return means
        
        
        
        
    def stat_median(self, *index, glob=False):
        """
        Find the medians of the columns specified by *index.
        
        Parameters
        ----------
            *index: zero or more ints.
                The indices specifying the columns of which the medians shall be found.
            
        Returns
        -------
            means: number or array-like
                The medians of the columns specified by *index. Has shape (len(index),:) or is a number if only one index is specified.
                
            glob: bool, optional
                If glob=False an array containing the median values of the columns specified by *index is returned. Otherwise the median among those columns is returned.
            
        Raises
        ------
            ValueError
                If an index is not smaller than Data.length.
        """

        if np.any(np.array(index) >= self.length):
            raise IndexError("At least one index is out of range for Data with length %d."%self.length)
        
        if len(index) == 0:
            if glob:
                return np.median(self.y)
            else:
                return np.median(self.y, axis=1)
        
        elif len(index) == 1:
            return np.median(self.y[index[0],:])
        
        else:
            medians = np.zeros(len(index))
            count = 0
            for i in index:
                if type(self.y) in (int, float):
                    medians[count] = self.y
                elif len(self.y.shape) == 1:
                    medians[count] = np.median(self.y[i])
                else:
                    medians[count] = np.median(self.y[i,:])
                count += 1
            if glob:
                return np.median(medians)
            else:
                return medians
        
        
        
    def stat_var(self, *index, glob=False):
        """
        Find the variances of the columns specified by *index.
        
        Parameters
        ----------
            *index: zero or more ints.
                The indices specifying the columns of which the variances shall be found.
                
            glob: bool, optional
                If glob=False an array containing the variance values of the columns specified by *index is returned. Otherwise the variance among those columns is returned.
            
        Returns
        -------
            vars: number or array-like
                The variances of the columns specified by *index. Has shape (len(index),:) or is a number if only one index is specified.
                
            
        Raises
        ------
            ValueError
                If an index is not smaller than Data.length.
        """

        if np.any(np.array(index) >= self.length):
            raise IndexError("At least one index is out of range for Data with length %d."%self.length)
        
        if len(index) == 0:
            if glob:
                return np.var(self.y)
            else:
                return np.var(self.y, axis=1)
        
        elif len(index) == 1:
            return np.var(self.y[index[0],:])
        
        else:
            varis = np.zeros(len(index))
            count = 0
            for i in index:
                if type(self.y) in (int, float):
                    varis[count] = self.y
                elif len(self.y.shape) == 1:
                    varis[count] = np.var(self.y[i])
                else:
                    varis[count] = np.var(self.y[i,:])
                count += 1
            if glob:
                return np.var(varis)
            else:
                return varis
        
        
        
    def stat_std(self, *index, glob=False):
        """
        Find the standard deviations of the columns specified by *index.
        
        Parameters
        ----------
            *index: zero or more ints.
                The indices specifying the columns of which the standard deviations shall be found.
                
            glob: bool, optional
                If glob=False an array containing the standard deviation values of the columns specified by *index is returned. Otherwise the standard deviation among those columns is returned.
            
        Returns
        -------
            std: number or array-like
                The standard deviations of the columns specified by *index. Has shape (len(index),:) or is a number if only one index is specified.
                
            
        Raises
        ------
            ValueError
                If an index is not smaller than Data.length.
        """

        if np.any(np.array(index) >= self.length):
            raise IndexError("At least one index is out of range for Data with length %d."%self.length)
        
        if len(index) == 0:
            if glob:
                return np.std(self.y)
            else:
                return np.std(self.y, axis=1)
        
        elif len(index) == 1:
            return np.std(self.y[index[0],:])
        
        else:
            stds = np.zeros(len(index))
            count = 0
            for i in index:
                if type(self.y) in (int, float):
                   stds[count] = self.y
                elif len(self.y.shape) == 1:
                    stds[count] = np.std(self.y[i])
                else:
                    stds[count] = np.std(self.y[i,:])
                count += 1
            if glob:
                return np.std(stds)
            else:
                return stds
            
            
    def stat_sum(self, *index, glob=False):
        """
        Find the sums of the columns specified by *index.
        
        Parameters
        ----------
            *index: zero or more ints.
                The indices specifying the columns of which the sums shall be found.
                
            glob: bool, optional
                If glob=False an array containing the sum values of the columns specified by *index is returned. Otherwise the sum among those columns is returned.
            
        Returns
        -------
            std: number or array-like
                The sums of the columns specified by *index. Has shape (len(index),:) or is a number if only one index is specified.
                
            
        Raises
        ------
            ValueError
                If an index is not smaller than Data.length.
        """

        if np.any(np.array(index) >= self.length):
            raise IndexError("At least one index is out of range for Data with length %d."%self.length)
        
        if len(index) == 0:
            if glob:
                return np.sum(self.y)
            else:
                return np.sum(self.y, axis=1)
        
        elif len(index) == 1:
            return np.sum(self.y[index[0],:])
        
        else:
            sums = np.zeros(len(index))
            count = 0
            for i in index:
                if type(self.y) in (int, float):
                   sums[count] = self.y
                elif len(self.y.shape) == 1:
                    sums[count] = np.sum(self.y[i])
                else:
                    sums[count] = np.sum(self.y[i,:])
                count += 1
            if glob:
                return np.sum(sums)
            else:
                return sums
            
    
    # ******************************************************** FITTING *******************************************************
    
    
    
    # ******************************************************** PLOTTING *******************************************************
    
    
    def plot(self, *index, axes=None, logx=False, logy=False, legend=True, linestyle='-', marker='.', xlabel=True, ylabel=True, title=None, linewidth=1.5, markersize=5):
        
        
        if np.any(np.array(index) >= self.length):
            raise IndexError("At least one index is out of range for Data with length %d."%self.length)
        
        
        if title != None:
            plt.suptitle(title)
        
        if axes == None:
            #plt.figure()
            ax = plt.subplot(1,1,1)
            ax.set_xlabel(self.xname)
            ax.set_ylabel(self.yname)
        else:
            ax = axes
        
        if logx and logy:
            command = ax.loglog
        elif logx and not logy:
            command = ax.semilogx
        elif not logx and logy:
            command = ax.semilogy
        else:
            command = ax.plot
        
        
        if len(index) == 0:
            rng = range(self.length)
        else:
            rng = index
            
        for i in rng:
            if legend:
                string = ''
                if self.properties[i] == None:
                    string = 'None'
                else:
                    for j in self.properties[i]:
                        string += str(j) + ':' + str(self.properties[i][j]) + ', '
                    
                command(self.x, self.y[i,:], label=string[0:-2], linestyle=linestyle, marker=marker, linewidth=linewidth, markersize=markersize)
        
                plt.legend()
            else:
                command(self.x, self.y[i,:], linestyle=linestyle, marker=marker)
                
              
              
              
              
              
    def plot_correl(self, index1, index2, axes=None, logx=False, logy=False, legend=True, linestyle='none', marker='.', xlabel=True, ylabel=True, title=None, linewidth=1.5, markersize=5):
        
        if index1 > self.length:
            raise ValueError("index1 is too large for Data with length %d."%self.length)
        if index2 > self.length:
            raise ValueError("index2 is too large for Data with length %d."%self.length)
        
        
        if title != None:
            plt.suptitle(title)
        

        if axes == None:
            ax = plt.subplot(1,1,1)
        else:
            ax = axes
            
        if xlabel:
            ax.set_xlabel(self.yname + ' y[%d,:]'%index1)
        if ylabel:
            ax.set_ylabel(self.yname + ' y[%d,:]'%index2)
        
        if logx and logy:
            command = ax.loglog
        elif logx and not logy:
            command = ax.semilogx
        elif not logx and logy:
            command = ax.semilogy
        else:
            command = ax.plot
            
        if legend:
            command(self.y[index1,:], self.y[index2,:], label='y[%d,:] vs y[%d,:]'%(index1, index2), linestyle=linestyle, marker=marker, linewidth=linewidth, markersize=markersize)
            plt.legend()
        else:
            command(self.y[index1,:], self.y[index2,:], linestyle=linestyle, marker=marker, linewidth=linewidth, markersize=markersize)
            
    
    
    
    
    
    
    def plot_correlmat(self, logx=False, logy=False, legend=False, linestyle='none', marker='.', xlabel=True, ylabel=True, title=None, linewidth=1.5, markersize=5, figsize=(10,7)):
        
        
        plt.figure(figsize=figsize)
        if title != None:
            plt.suptitle(title)
            
        for i in range(self.length):
            for j in range(self.length):
                
                ax = plt.subplot(self.length, self.length, i*self.length+j+1)
                
                if logx and logy:
                    command = ax.loglog
                elif logx and not logy:
                    command = ax.semilogx
                elif not logx and logy:
                    command = ax.semilogy
                else:
                    command = ax.plot
                
                
                if xlabel and i == self.length-1:
                    ax.set_xlabel('y%d'%j)
                if ylabel and j == 0:
                    ax.set_ylabel('y%d'%i)
                    
                if i < self.length-1:
                    ax.set_xticks([])
                if j > 0:
                    ax.set_yticks([])
                    
                if legend:
                    command(self.y[i,:], self.y[j,:], label='y[%d,:] vs y[%d,:]'%(i,j), linestyle=linestyle, marker=marker, linewidth=linewidth, markersize=markersize)
                else:
                    command(self.y[i,:], self.y[j,:], linestyle=linestyle, marker=marker, linewidth=linewidth, markersize=markersize)
                    
                
                    
                    
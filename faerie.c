#include "Python.h"
#include <stdlib.h>

typedef struct node{
    long entity;
    long position;
} Node;

//rebalance the heap
static void down(Node *heap,long len, long i){
    long min;
    while(i*2<=len){
        if(i*2+1 > len)
            min = i * 2;
        else{
            if(heap[i*2-1].entity<heap[i*2].entity)
             min = i * 2;
            else
                min = i * 2 + 1;
        }
        if(heap[i-1].entity>heap[min-1].entity){
            Node temp = heap[i-1];
            heap[i-1] = heap[min-1];
            heap[min-1] = temp;
        }
        i = min;
    }
}
//turn a list to a min heap
static void heapify(long len,Node *heap){
    long i = len/2+1;
    while(i>0){
        down(heap,len,i);
        i--;
    }
}
//replace the top entity with [i,j]
static void replace(Node *heap,long len, long e,long p){
    heap[0].entity = e;
    heap[0].position = p;
    down(heap,len,1);
}

static long BinaryShift(long i, long j, long upe,long Tl,long *Pe,long psize){
    long lower = i;
    long upper = j;
    while(lower<=upper){
        long mid = floor((upper+lower)/2);
        if((Pe[j] + mid - i - Pe[mid] + 1) >upe)
            lower = mid + 1;
        else
            upper = mid - 1;
    }
    i = lower;
    j = i + Tl -1;
    if (j>=psize){
        return -1;
    }
    if((Pe[j]-Pe[i]+1)>upe)
        return BinaryShift(i,j,upe,Tl,Pe,psize);
    else
        return i;
}

static PyObject* PyDicListGetItem(PyObject *list, PyObject *dict,long i){
    if (list == Py_None || list == NULL)
        printf("%s\n","dll NULL" );
    if (dict == Py_None || dict == NULL)
        printf("%s\n","dld NULL" );
    if (PyList_GetItem(list,i) == NULL){
        printf("%d,%d\n",i, PyList_GET_SIZE(list));
        printf("%s\n","cannot get list item" );
        return NULL;
    }
    PyObject *listitem = NULL;
    listitem = PyList_GetItem(list,i);
    if (PyDict_GetItem(dict,listitem) == NULL){
        printf("%s\n","cannot get dictionary item" );
        return NULL;
    }
    if(PyDict_Contains(dict,listitem) != 1){
        printf("%s\n","key not found" );
    }
    PyObject *dictitem = NULL;
    dictitem = PyDict_GetItem(dict,listitem);
    return dictitem;
}

static PyObject* PyLiListGetItem(PyObject *list, long i,long j){
    if (list == Py_None)
        printf("%s\n","lili NULL" );
    if (PyList_GetItem(list,i) == NULL){
        printf("%d,%d\n",i, PyList_GET_SIZE(list));
        printf("%s\n","cannot get list item" );
        return NULL;
    }
    PyObject *listitem = NULL;
    listitem = PyList_GetItem(list,i);
    if (PyList_GetItem(listitem,j) == Py_None){
        printf("%s\n","cannot get dictionary item" );
        return NULL;
    }
    PyObject *list2item = NULL;
    list2item = PyList_GetItem(listitem,j);
    return list2item;
}

static long pyGetint(PyObject *ob){
    if (ob == Py_None)
        printf("%s\n","int NULL" );
    if (PyInt_Check(ob)){
        long i = PyInt_AsLong(ob);
        return i;
    }
    else{
        printf("%s\n","pyint_error" );
        return NULL;
    }
}

static PyObject *
he_getcandidates(PyObject *self, PyObject *args)
{
    //list:the heap; entity_len:the dictionary of entity length; inlist_len: the dictionary of inverted list length; inindex: the ids of entities; result: the return result; tokens: list of tokens in document.    
    PyObject *list = NULL;
    PyObject *entity_len = NULL;
    PyObject *inlist_len = NULL;
    PyObject *inindex = NULL;
    PyObject *inlist = NULL;
    PyObject *tokens = NULL;
    //len: length of heap; loe: length of entity; los: length of document tokens; e: top entity in heap; [ei,pi]:next entity after poping e; psize: position array size.
    int len,loe,los,e,ei,pi,psize,i,j,l,maxentitylen;
    //unified threshold
    float T;
    float threshold = 0.8;
    // PyObject *result = PyList_New(0);
    if (!PyArg_ParseTuple(args, "OOOOOOii", &list,&entity_len,&inlist_len,&inindex,&inlist,&tokens,&los,&maxentitylen))
        return NULL;
    //current_index: this shows the current entity index in inverted list.
    int *current_index= PyMem_New(int,los);
    //Pe: position list
    int *Pe = PyMem_New(int,los);
    for(i=0;i<los;i++){
        current_index[i] = 0;
    }
    len = PyList_GET_SIZE(list);
    Node *heap = PyMem_New(Node,len);
    for(i=0;i<len;i++){
        PyObject *entity = PyLiListGetItem(list,i,0);
        long e = pyGetint(entity);
        PyObject *position = PyLiListGetItem(list,i,1);
        long p = pyGetint(position);
        heap[i].entity = e;
        heap[i].position = p;
    }
    heapify(len,heap);
    e = heap[0].entity;
    //occurance count matrix
    int **occur;
    //lower and upper bound of the valid substring of document according to e
    int lowe,upe;
    psize = 0;
    PyObject *lenofen = PyDicListGetItem(inindex,entity_len,e);
    loe = pyGetint(lenofen);
    lowe = ceil(loe*threshold);
    upe = floor(loe/threshold);
    occur = PyMem_New(int*,los);
    maxentitylen = floor(maxentitylen/threshold) - ceil(maxentitylen*threshold) + 1;
    for(j=0;j<los;j++){
        occur[j] = PyMem_New(int,maxentitylen);  
        for(i=0;i<maxentitylen;i++)
            occur[j][i] = 0;
    }
    while(1){
        ei = heap[0].entity;
        pi = heap[0].position;
        // printf("%d,%d\n",ei,pi );
        if(ei == 237392 || pi == -1){
            for (i=0;i<los;i++){
                PyMem_Del(occur[i]); 
                occur[i] = NULL;   
            }         
            PyMem_Del(occur);
            occur = NULL;
            PyMem_Del(Pe);
            Pe = NULL;
            PyMem_Del(current_index);
            current_index = NULL;
            PyMem_Del(heap);
            heap = NULL;
            break;
        }
        if(ei == e){
            //insert the position i and sort the list Pe.
            if(psize == 0){
                Pe[psize] = pi;
            }
            else if(pi<Pe[psize-1]){
                i = psize-1;
                //Pe[psize] = Pe[psize-1];
                while(pi<Pe[i]){
                    Pe[i+1] = Pe[i];
                    i--;
                }
                Pe[i+1] = pi;
            }else
                Pe[psize] = pi;
            psize++;
            int k;
            for(l=0;l<=upe-lowe;l++){
                if(pi-l-lowe+1>=0)
                    k = pi-l-lowe+1;
                else
                    k = 0;
                for(i=k;i<=pi;i++)
                    occur[i][l]++;
            }
        }
        else{
            if(psize>=lowe){
                i = 0;
                while(i<=psize-lowe){
                    j = i+lowe-1;
                    if(Pe[j]-Pe[i]<=upe){
                        //Binary Span
                        int lower = j;
                        int upper = i+upe-1;
                        while(lower<upper){
                            int mid = ceil((upper+lower)/2);
                            if(Pe[mid]-Pe[i]+1>upe)
                                upper = mid - 1;
                            else
                                lower = mid + 1;
                        }
                        if (upper>=psize-1){
                            upper = psize-1;
                            int slen = Pe[upper] - Pe[i] + 1;
                            if(lowe<=slen && slen<=upe){
                                T = ceil((loe+los)*(threshold/(1+threshold)));
                                if (occur[Pe[i]][slen-lowe] >= T){
                                    // PyList_Append(result,Py_BuildValue("[i,i,i]", e, Pe[i],Pe[upper])); 
                                }                                                               
                            }
                            break;
                        }
                        int slen = Pe[upper] - Pe[i] + 1;
                        if(lowe<=slen && slen<=upe){
                            T = ceil((loe+los)*(threshold/(1+threshold)));
                            if (occur[Pe[i]][slen-lowe] >= T){
                                // PyList_Append(result,Py_BuildValue("[i,i,i]", e, Pe[i],Pe[upper])); 
                            }
                        }
                        i++;
                    }else{
                        i = BinaryShift(i,j,upe,lowe,Pe,psize);
                        if (i==-1)
                            break;                        
                    }
                }
            }
            e = ei;
            PyObject *lenofen = PyDicListGetItem(inindex,entity_len,e);
            loe = pyGetint(lenofen);
            lowe = ceil(loe*threshold);
            upe = floor(loe/threshold);            
            psize = 0;
            Pe[psize] = pi;
            psize++;
            for(j=0;j<los;j++){
                for(i=0;i<maxentitylen;i++)
                    occur[j][i] = 0;
            }
        }
        PyObject *invertedlistpilen = PyDicListGetItem(tokens,inlist_len,pi);
        if (pyGetint(invertedlistpilen)> current_index[pi]+1){
            current_index[pi]++;
            if(pi>=los)
                printf("%s\n","out of range" );
            PyObject *invertedlistpi = PyDicListGetItem(tokens,inlist,pi);
            PyObject *nextentity = PyList_GetItem(invertedlistpi,current_index[pi]);
            if(nextentity == NULL || nextentity == Py_None)
                printf("%s\n","wrong int" );
            replace(heap,len,pyGetint(nextentity),pi);
        }
        else{
            replace(heap,len,237392,-1);
        }
    }
    Py_INCREF(Py_None);
    return Py_None;
}
 
static PyMethodDef faerie_methods[] = {
    {"getcandidates", he_getcandidates, METH_VARARGS, "return candidates"},
    {NULL, NULL}
};

// /* Python 3.x code */
 
// static struct PyModuleDef faeriemodule = {
//    PyModuleDef_HEAD_INIT,
//    "faerie",   /* name of module */
//    "faerie_doc", /* module documentation, may be NULL */
//    -1,        size of per-interpreter state of the module,
//                 or -1 if the module keeps state in global variables. 
//    faerie_methods
// };

// PyMODINIT_FUNC
// PyInit_faerie(void)
// {
//     (void) PyModule_Create(&faeriemodule);
// }

/* Python 2.x code */

PyMODINIT_FUNC
initfaerie(void)
{
    Py_InitModule("faerie", faerie_methods);
}
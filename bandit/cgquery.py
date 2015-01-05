import click
import yaml
import logging
from pprint import pprint

try:
    import asciitree
    def children(n):
        for x in n.itervalues():
            for y in x:
                yield y

    def treeprint(t):
        asciitree.draw_tree(t, children, lambda n: n.iterkeys().next())

    #pprint = treeprint
except Exception:
    pass

logger = logging.getLogger()

@click.group()
def cli():
    pass

def load_call_graph(path):
    logger.debug('Loading {}'.format(path))
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def build_reverse_call_graph(cg):
    calledby = {}
    for (caller, callees) in cg.iteritems():
        for callee in callees:
            if callee in calledby:
                calledby[callee].update([caller])
            else:
                calledby[callee] = set([ caller ])
    with open("/tmp/bandit.reverse", "w") as f:
        yaml.dump(calledby, f)
    return calledby

@cli.command()
@click.argument('cgdb_path')
@click.argument('qualname')
def callers(cgdb_path, qualname):
    cg = load_call_graph(cgdb_path)
    calledby = build_reverse_call_graph(cg)

    def search(callee, calledby, lvl):
        if lvl > 5:
            return { callee + ' depth exceeded' : [] }

        if callee not in calledby:
            return { callee : [] }

        result = {}
        result[callee] = []
        for caller in calledby[callee]:
            tree = search(caller, calledby, lvl+1)
            result[callee].append(tree)

        return result

    call_tree = search(qualname, calledby, 0) 
    pprint(call_tree)

@cli.command()
@click.argument('cgdb_path')
@click.argument('qualname')
def callees(cgdb_path, qualname):
    print('callees')


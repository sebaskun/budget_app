const buildTree = (tasks) => {
  let tree = []
  let parents = []

  function getNodeById (id, node) {
    let reduce = [].reduce
    function runner(result, node){
        if(result || !node) return result
        return node.uid === id && node || //is this the proper node?
            runner(null, node.children) || //process this nodes children
            reduce.call(Object(node), runner, result)  //maybe this is some ArrayLike Structure
    }
    return runner(null, node)
  }


  tasks.forEach((element, index) => {
    let current_level = element.outline_level
    let next_level = (index + 1) < tasks.length ? tasks[index+1].outline_level : 0
    let parent = {}
    let uid = 0

    // if (current_level > 0){
      // Si el nivel del elemento actual es menor que el nivel del elemento siguiente
      // entonces el elemento actual es padre y lo
      // guardamos en el stack
      if (!parents.length || current_level == 0){
        tree.push(element)
      }else{
        uid = parents[parents.length - 1].uid
        // parent = tree.filter(nodo => nodo.uid == uid)[0]
        parent = getNodeById(uid, tree)
        if (!("children" in parent)){
          parent.children = []
        }
        parent.children.push(element)
      }
      if (current_level < next_level){
        /*for (var i=0;i<(next_level-current_level);i++)*/
          parents.push(element)
      }else{
        if (current_level>next_level){
          for (var i=0;i<(current_level-next_level);i++)
            parents.pop()
        }
      }
      // tree.push(element)
    // }else{
    //   tree.push(element)
    // }
  })
  return tree
}

export default buildTree

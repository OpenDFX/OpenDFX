// Give each checklist checkbox ("- [ ] item" in Markdown) an accessible name: the text of its item.
// Without it, a screen reader announces only "checkbox" (WCAG 2.2, 1.3.1 and 4.1.2).
function text(node) {
  if (node.type === 'text') return node.value;
  return (node.children || []).map(text).join('');
}

function walk(node, fn) {
  fn(node);
  (node.children || []).forEach((child) => walk(child, fn));
}

export default function labelTaskCheckboxes() {
  return (tree) => {
    walk(tree, (node) => {
      if (node.type !== 'element' || node.tagName !== 'li') return;
      const props = node.properties || {};
      const classes = [].concat(props.className || []);
      if (!classes.includes('task-list-item')) return;
      let box;
      walk(node, (n) => {
        if (!box && n.type === 'element' && n.tagName === 'input' && n.properties?.type === 'checkbox') box = n;
      });
      if (box) box.properties.ariaLabel = text(node).replace(/\s+/g, ' ').trim();
    });
  };
}

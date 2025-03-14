// Hiển thị/ẩn nút "Xóa nhiều" dựa trên checkbox được chọn
function toggleDeleteButton() {
  const checkboxes = document.querySelectorAll(
    'input[name="note-checkbox"]:checked'
  );
  const deleteButton = document.getElementById("delete-selected");
  deleteButton.style.display = checkboxes.length > 0 ? "block" : "none";
}

// Xóa nhiều ghi chú
const deleteSelectedNotes = () => {
  const checkboxes = document.querySelectorAll(
    'input[name="note-checkbox"]:checked'
  );
  const noteIds = Array.from(checkboxes).map((cb) => parseInt(cb.value));

  if (noteIds.length === 0) {
    alert("Vui lòng chọn ít nhất một ghi chú để xóa!");
    return;
  }

  if (!confirm(`Bạn có chắc muốn xóa ${noteIds.length} ghi chú không?`)) {
    return;
  }

  console.log(`Đang xóa các ghi chú với IDs: ${noteIds}`);
  fetch("/delete-note", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ note_ids: noteIds }),
  })
    .then((response) => {
      if (!response.ok) throw new Error("Lỗi khi xóa ghi chú");
      return response.json();
    })
    .then((data) => {
      if (data.success) {
        console.log(`Xóa ${noteIds.length} ghi chú thành công`);
        noteIds.forEach((noteId) => {
          const noteElement = document.querySelector(`input[value="${noteId}"]`)
            .parentElement.parentElement;
          noteElement.style.transition = "opacity 0.3s";
          noteElement.style.opacity = "0";
        });
        setTimeout(() => {
          window.location.reload(); // Tải lại để hiển thị flash
        }, 300);
      } else {
        console.error("Xóa thất bại:", data.message);
        alert("Không thể xóa các ghi chú: " + data.message);
      }
    })
    .catch((error) => {
      console.error("Lỗi:", error);
      alert("Có lỗi xảy ra khi xóa các ghi chú!");
    });
};

// Chỉnh sửa ghi chú
function editNote(noteId) {
  const noteTextElement = document.getElementById(`note-text-${noteId}`);
  const currentText = noteTextElement.textContent;

  // Tạo input để chỉnh sửa
  const input = document.createElement("input");
  input.type = "text";
  input.value = currentText;
  input.className = "form-control";
  input.style.width = "70%";

  // Thay thế nội dung hiện tại bằng input
  noteTextElement.replaceWith(input);
  input.focus();

  // Khi người dùng nhấn Enter hoặc mất focus, lưu lại
  input.addEventListener("blur", saveNote);
  input.addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
      saveNote();
    }
  });

  function saveNote() {
    const newText = input.value.trim();
    if (newText && newText !== currentText) {
      fetch("/update-note", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ note_id: noteId, data: newText }),
      })
        .then((response) => {
          if (!response.ok) throw new Error("Lỗi khi cập nhật ghi chú");
          return response.json();
        })
        .then((data) => {
          if (data.success) {
            console.log(`Cập nhật ghi chú ${noteId} thành công`);
            const newSpan = document.createElement("span");
            newSpan.id = `note-text-${noteId}`;
            newSpan.style = "color: #333; font-size: 16px";
            newSpan.textContent = newText;
            input.replaceWith(newSpan);
          } else {
            console.error("Cập nhật thất bại:", data.message);
            alert("Không thể cập nhật ghi chú: " + data.message);
            input.replaceWith(noteTextElement); // Khôi phục nếu lỗi
          }
        })
        .catch((error) => {
          console.error("Lỗi:", error);
          alert("Có lỗi xảy ra khi cập nhật ghi chú!");
          input.replaceWith(noteTextElement); // Khôi phục nếu lỗi
        });
    } else {
      input.replaceWith(noteTextElement); // Khôi phục nếu không thay đổi
    }
  }
}

// Gọi hàm toggleDeleteButton khi trang tải để kiểm tra trạng thái ban đầu
document.addEventListener("DOMContentLoaded", toggleDeleteButton);

document.getElementById("avatarInput").addEventListener("change", function () {
  document.getElementById("avatarForm").submit();
});
